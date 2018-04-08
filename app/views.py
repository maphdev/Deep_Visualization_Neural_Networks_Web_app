# Copyright 2018 (C) A. Brabant A. Delasalle L. Leduc M. Philippot

# This file is part of P&P Deep-Vis.

# P&P Deep-Vis is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.

# P&P Deep-Vis is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.

# You should have received a copy of the GNU Lesser General Public License along
# with P&P Deep-Vis; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import json
import tempfile
import matplotlib.image as mpimg

from app import app
from flask import render_template, request, flash, url_for, redirect, session
from werkzeug.utils import secure_filename

from .module.visualization.keras_vis_visualization import *
from .module.visualization.utils import *

from .module.database.datafile import *

# important path
DefaultUser = "defaultUser"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(os.path.join(APP_ROOT, 'static', 'database')):
    os.makedirs(os.path.join(APP_ROOT, 'static', 'database'))
DB = DataFile(os.path.join(APP_ROOT, 'static', 'database'))
DB.addUser(DefaultUser)

# return true if the model's extension is allowed, false otherwise
def allowed_model(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in set(['h5'])

def list_of_files(list, extend=None):
    list_of_files = {}
    for filename in list:
        list_of_files[filename] = filename + extend
    return list_of_files

# generate a conventional name for the result image for Reason
def generate_image_name_for_Reason(model_name, image_name, layer, unit):
    return os.path.splitext(model_name)[0] + "_Reason_" + os.path.splitext(image_name)[0] + "_" + str(layer) + "_" + str(unit)

# generate a conventional name for the result image for MaxOut
def generate_image_name_for_MaxOut(model_name, layer, unit, iter):
    return os.path.splitext(model_name)[0] + "_MaxOut_" + str(layer) + "_" + str(unit) + "_" + str(iter)

# return home page
@app.route('/')
def index():
    return render_template('index.html')

# return models page
@app.route('/models/')
def models():
    return render_template('models.html', files=list_of_files(DB.selectAllUserModels(DefaultUser), '.h5'))

# retourn about page
@app.route('/about/')
def about():
    return render_template('about.html')

# when a model is uploaded to the server
@app.route('/upload_model/', methods=['POST'])
def upload_model():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'model' not in request.files:
            flash('No selected model.')
            return redirect(url_for('models'))

        file = request.files['model']

        # check if the extension is allowed
        if not allowed_model(file.filename):
            flash('Model\'s extension is incorrect.')
            return redirect(url_for('models'))

        # if there is a model file and the extension is correct
        if file and allowed_model(file.filename):
            filename = secure_filename(file.filename)
            # if the name is already in the server
            if os.path.splitext(filename)[0] in DB.selectAllUserModels(DefaultUser):
                flash('A model with the same name already exists. If it is not the same model, please rename your model before uploading it or delete it.')
                return redirect(url_for('models'))
            else:
                # the model is saved
                try:
                    model_path = DB.addModel(user=DefaultUser, model_name=os.path.splitext(filename)[0], model=file)
                    model = selected_model(model_path)
                    model_json = get_model_json(model)
                    DB.addModelJson(user=DefaultUser, model_name=os.path.splitext(filename)[0], model_json=model_json)
                except Exception as e:
                    flash(str(e))
                    return redirect(url_for('models'))

    return render_template('models.html', files=list_of_files(DB.selectAllUserModels(DefaultUser), '.h5'))

# when a model is deleted of the server
@app.route('/delete_model/', methods=['POST'])
def delete_model():
    model_name = request.form["filename"]
    DB.removeModel(user=DefaultUser, model_name=os.path.splitext(model_name)[0])
    return render_template('models.html', files=list_of_files(DB.selectAllUserModels(DefaultUser), '.h5'))

# return params visualization page
@app.route('/visualisations/', methods=['GET', 'POST'])
def visualisations():
    if request.method == 'POST':
        filename = request.form['filename']
        session['model_name'] = filename
    else:
        filename = session.get('model_name', None)
    json_name = DB.selectUserModelJson(user=DefaultUser, model_name=os.path.splitext(filename)[0])[len(APP_ROOT):]
    print(json_name)
    return render_template('visualisations.html', filename=filename, json_name=json_name)

@app.route('/result_reason/', methods=['GET', 'POST'])
def result_reason():
    # retrieve elements from form
    # model
    model_name = session.get('model_name', None)
    # image name
    image_file = request.files['image']
    image_name = secure_filename(image_file.filename)

    if not request.form.get('predict'):
        # layer
        layer_num = request.form['layer']
        # unit
        unit_num = request.form['unit']
        # generate image name
        img_result_name = generate_image_name_for_Reason(model_name, image_name, layer_num, unit_num)
        if request.form.get('cache'):
            try:
                filename = DB.selectUserModelvis(user=DefaultUser, model_name=os.path.splitext(model_name)[0], vis='reason', img_name=img_result_name)
                return render_template('result.html', filename=filename[len(os.path.join(APP_ROOT, 'static')+os.sep):])
            except Exception:
                pass

    # check and load model and image
    image_path = os.path.join(APP_ROOT, 'static', 'tmp', next(tempfile._get_candidate_names()) + '.'+ os.path.splitext(image_name)[1])
    image_file.save(image_path)
    try:
        model = selected_model(DB.selectUserModel(user=DefaultUser, model_name=os.path.splitext(model_name)[0]))
        image = load_img_for_model(model, image_path)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('visualisations'))

    # layer and unit, if it's predicted or choosed by user
    if request.form.get('predict'):
        # layer
        layer_num = len(model.layers)-1
        # unit
        unit_num = predict(model, image)['class']
        # generate image name
        img_result_name = generate_image_name_for_Reason(model_name, image_name, layer_num, unit_num)

    if request.form.get('cache'):
        try:
            filename = DB.selectUserModelvis(user=DefaultUser, model_name=os.path.splitext(model_name)[0], vis='reason', img_name=img_result_name)
            return render_template('result.html', filename=filename[len(os.path.join(APP_ROOT, 'static')+os.sep):])
        except Exception:
            pass
    # check parameters and start visualisation
    try:
        # parameters
        layer = selected_layer(model, int(layer_num))
        unit = selected_filter(model, layer, int(unit_num))
        # visualisation
        visu = ReasonKerasVis()
        image_mod = visu.apply(model, image, layer, unit)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('visualisations'))

    # save result
    try:
        DB.removeVisualization(user=DefaultUser, model_name=os.path.splitext(model_name)[0], vis='reason', img_name=img_result_name)
    except Exception:
        pass

    filename = DB.addVisualization(user=DefaultUser, model_name=os.path.splitext(model_name)[0], vis='reason', img_name=img_result_name, img=image_mod)

    # delete original image
    os.remove(image_path)
    return render_template('result.html', filename=filename[len(os.path.join(APP_ROOT, 'static')+os.sep):])

@app.route('/result_maxout/', methods=['GET', 'POST'])
def result_maxout():
    # retrieve elements from form
    # model
    model_name = session.get('model_name', None)
    # layer
    layer_num = request.form['layer']
    # unit
    unit_num = request.form['unit']
    # iterations
    iterations_num = request.form['iterations']

    # check in cache if image is already available
    img_result_name = generate_image_name_for_MaxOut(model_name, layer_num, unit_num, iterations_num)
    try:
        filename = DB.selectUserModelvis(user=DefaultUser, model_name=os.path.splitext(model_name)[0], vis='maxout', img_name=img_result_name)
        return render_template('result.html', filename=filename[len(os.path.join(APP_ROOT, 'static')+os.sep):])
    except Exception:
        pass

    # check and load elements
    try:
        model = selected_model(DB.selectUserModel(user=DefaultUser, model_name=os.path.splitext(model_name)[0]))
        layer = selected_layer(model, int(layer_num))
        unit = selected_filter(model, layer, int(unit_num))
        max_iter = selected_interation(int(iterations_num))
        # start visualization
        visu = MaxoutKerasVis()
        image_mod = visu.apply(model, layer, unit, max_iter)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('visualisations'))

    # save result
    filename = DB.addVisualization(user=DefaultUser, model_name=os.path.splitext(model_name)[0], vis='maxout', img_name=img_result_name, img=image_mod)

    return render_template('result.html', filename=filename[len(os.path.join(APP_ROOT, 'static')+os.sep):])
