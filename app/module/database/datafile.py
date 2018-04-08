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

import os, json, shutil, errno
import matplotlib.image as mpimg

from .exception import *
from .database import DataBase

from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from keras.models import load_model

class DataFile( DataBase ):

    def __init__(self, data_base_path):
        self.data_base_path = data_base_path
        for user in os.listdir(data_base_path):
            for model_name in os.listdir(os.path.join(data_base_path, user)):
                path = os.path.join(data_base_path, user, model_name)
                if not os.path.exists(os.path.join(path, model_name + '.h5')):
                    shutil.rmtree(path, ignore_errors=True)
                elif not os.path.exists(os.path.join(path, model_name + '.json')):
                    shutil.rmtree(path, ignore_errors=True)

    def addUser(self, user):
        path = os.path.join(self.data_base_path, user)
        if not os.path.exists(path):
            os.makedirs(path)

    def removeUser(self, user):
        path = os.path.join(self.data_base_path, user)
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)
        else:
            raise UserNotFoundError()

    def addModel(self, user, model_name, model):
        if not os.path.exists(os.path.join(self.data_base_path, user)):
            raise UserNotFoundError()
        model_name = secure_filename(model_name)
        path = os.path.join(self.data_base_path, user, model_name)
        if not os.path.exists(path):
            os.makedirs(path)
            model.save(os.path.join(path, model_name + '.h5'))
        return os.path.join(path, model_name + '.h5')

    def removeModel(self, user, model_name):
        if not os.path.exists(os.path.join(self.data_base_path, user)):
            raise UserNotFoundError()
        path = os.path.join(self.data_base_path, user, model_name)
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)
        else:
            raise ModelNotFoundError()

    def addModelJson(self, user, model_name, model_json):
        if not os.path.exists(os.path.join(self.data_base_path, user)):
            raise UserNotFoundError()
        if not os.path.exists(os.path.join(self.data_base_path, user, model_name)):
            raise ModelNotFoundError()
        path = os.path.join(self.data_base_path, user, model_name, model_name + '.json')
        if not os.path.exists(path):
            file = open(path, "w")
            file.write(model_json)
            file.close()
        return path

    def removeModelJson(self, user, model_name):
        if not os.path.exists(os.path.join(self.data_base_path, user)):
            raise UserNotFoundError()
        if not os.path.exists(os.path.join(self.data_base_path, user, model_name)):
            raise ModelNotFoundError()
        path = os.path.join(self.data_base_path, user, model_name, model_name + '.json')
        if os.path.exists(path):
            os.remove(path)

    def addVisualization(self, user, model_name, vis, img_name, img):
        if not os.path.exists(os.path.join(self.data_base_path, user)):
            raise UserNotFoundError()
        if not os.path.exists(os.path.join(self.data_base_path, user, model_name)):
            raise ModelNotFoundError()
        path = os.path.join(self.data_base_path, user, model_name, vis)
        if not os.path.exists(path):
            os.makedirs(path)
        filename = secure_filename(img_name)
        path = os.path.join(path, filename + '.jpg')
        if not os.path.exists(path):
            mpimg.imsave(path, img)
        return os.path.join(path)

    def removeVisualization(self, user, model_name, vis, img_name):
        if not os.path.exists(os.path.join(self.data_base_path, user)):
            raise UserNotFoundError()
        if not os.path.exists(os.path.join(self.data_base_path, user, model_name)):
            raise ModelNotFoundError()
        name = os.path.join(self.data_base_path, user, model_name, vis, img_name + '.jpg')
        if os.path.exists(name):
            os.remove(name)
            path = os.path.join(self.data_base_path, user, model_name, vis)
            if len(os.listdir(path)) == 0:
                shutil.rmtree(path, ignore_errors=True)
        else:
            raise VisuNotFoundError()

    def selectUserModel(self, user, model_name):
        if not os.path.exists(os.path.join(self.data_base_path, user)):
            raise UserNotFoundError()
        if not os.path.exists(os.path.join(self.data_base_path, user, model_name)):
            raise ModelNotFoundError()
        path = os.path.join(self.data_base_path, user, model_name, model_name + '.h5')
        if not os.path.exists(path):
            shutil.rmtree(os.path.join(self.data_base_path, user, model_name), ignore_errors=True)
            raise ModelNotFoundError()
        return path

    def selectUserModelJson(self, user, model_name):
        if not os.path.exists(os.path.join(self.data_base_path, user)):
            raise UserNotFoundError()
        if not os.path.exists(os.path.join(self.data_base_path, user, model_name)):
            raise ModelNotFoundError()
        path = os.path.join(self.data_base_path, user, model_name, model_name + '.json')
        if not os.path.exists(path):
            shutil.rmtree(os.path.join(self.data_base_path, user, model_name), ignore_errors=True)
            raise ModelNotFoundError()
        return path

    def selectUserModelvis(self, user, model_name, vis, img_name):
        if not os.path.exists(os.path.join(self.data_base_path, user)):
            raise UserNotFoundError()
        if not os.path.exists(os.path.join(self.data_base_path, user, model_name)):
            raise ModelNotFoundError()
        path = os.path.join(self.data_base_path, user, model_name, vis, img_name + '.jpg')
        if not os.path.exists(path):
            raise VisuNotFoundError()
        return path

    def selectAllUsers(self):
        return os.listdir(self.data_base_path)

    def selectAllUserModels(self, user):
        if not os.path.exists(os.path.join(self.data_base_path, user)):
            raise UserNotFoundError()
        return os.listdir(os.path.join(self.data_base_path, user))

    def selectAllUserModelVis(self, user, model_name):
        if not os.path.exists(os.path.join(self.data_base_path, user)):
            raise UserNotFoundError()
        if not os.path.exists(os.path.join(self.data_base_path, user, model_name)):
            raise ModelNotFoundError()
        result = []
        path = os.path.join(self.data_base_path, user, model_name)
        result.extend(os.listdir(path))
        return result

    def selectAllUserModelVisImg(self, user, model_name, vis):
        if not os.path.exists(os.path.join(self.data_base_path, user)):
            raise UserNotFoundError()
        if not os.path.exists(os.path.join(self.data_base_path, user, model_name)):
            raise ModelNotFoundError()
        result = []
        path = os.path.join(self.data_base_path, user, model_name, vis)
        if os.path.exists(path):
            result.extend(os.listdir(path))
        return result
