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

import os, sys, errno, json

import numpy as np

from keras import backend as K
from keras.models import load_model, Sequential

from skimage import io, transform

from .exception import *

def selected_model(path):
    """ Charge un modèle depuis le disque dur
    Args:
        path = chemin de l'image (str)
    Returns:
        keras.Model
    Raises:
        FileNotFoundError
    """
    if os.path.exists(path):
        return load_model(path)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

# Fonction load_img de keras-vis, utilise le package skimage
def load_img(path, grayscale=False, target_size=None):
    """ Charge une image depuis le disque dur
    Args:
      path = chemin de l'image (str)
      grayscale: True, converti en image de niveaux de gris (Default value = False)
      target_size: (w, h) redimensionne. (Default value = None)
    Returns:
        numpy image
    """
    img = io.imread(path, grayscale)
    if target_size:
        img = transform.resize(img, target_size, preserve_range=True).astype('uint8')
    return img

def load_img_for_model(model, path):
    """ Charge une image depuis le disque
    et la redimensionne en fonction de l'input du modèle
    Args:
        model = keras.Model
        path =  chemin de l'image (str)
    Returns:
        numpy image
    Raises:
        FileNotFoundError
    """
    if os.path.exists(path):
        shape = model.layers[0].input_shape
        if K.image_data_format() == 'channels_first':
            if shape[len(shape)-1] == 1:
                image = load_img(path, grayscale=True, target_size=(int(model.input.shape[2]), int(model.input.shape[3]), int(model.input.shape[4])))
            else:
                image = load_img(path, target_size=(int(model.input.shape[2]), int(model.input.shape[3]), int(model.input.shape[4])))
            image = image[:,:,0:shape[len(shape)-1]]
            image = image.reshape(model.input.shape[2], model.input.shape[3], model.input.shape[4])
        elif K.image_data_format() == 'channels_last':
            if shape[len(shape)-1] == 1:
                image = load_img(path, grayscale=True, target_size=(int(model.input.shape[1]), int(model.input.shape[2]), int(model.input.shape[3])))
            else:
                image = load_img(path, target_size=(int(model.input.shape[1]), int(model.input.shape[2]), int(model.input.shape[3])))
            image = image[:,:,0:shape[len(shape)-1]]
            image = image.reshape(model.input.shape[1], model.input.shape[2], model.input.shape[3])
        return image
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

def selected_layer(model, layer):
    """ Verifie la validité du layer passé en argument,
    vis-à-vis du modèle
    Args:
        model = keras.Model
        layer = int in range(0, len(model.layers))
    Returns:
        layer
    Raises:
        FileNotFoundError
    """
    # -1 est par defaut le dernier layer, le layer de prediction
    if(layer == -1):
        return -1
    if layer in range(0, len(model.layers)):
        return layer
    else:
        raise LayerOutOfRangeError(layer, len(model.layers))

# Fonction get_num_filters de keras-vis
def get_num_filters(layer):
    """ Determine le nombre d'unités du layer keras.
    Args:
        model.layers[x]: le layer keras.
    Returns:
        Total d'unités du layer
    """
    # Handle layers with no channels.
    if K.ndim(layer.output) == 2:
        return K.int_shape(layer.output)[-1]

    channel_idx = 1 if K.image_data_format() == 'channels_first' else -1
    return K.int_shape(layer.output)[channel_idx]

def selected_filter(model, layer, filter):
    """ Verifie la validité du filter passé en argument
    vis-à-vis du modèle et du layer
    Args:
        model = keras.Model
        layer = int in range(0, len(model.layers))
        filter = int in range(0, get_num_filters(model.layers[layer]))
    Returns:
        filter
    Raises:
        FilterOutOfRangeError
    """
    numberOfFilters = get_num_filters(model.layers[layer])
    if filter in range(0, numberOfFilters):
        return filter
    else:
        raise FilterOutOfRangeError(filter, numberOfFilters)

def selected_interation(nb_iter):
    """ Verifie la validite du nombre d'itération passe en argument
    Args:
        nb_iter: nombre d'itération (int)
    Returns:
        nb_iter
    Raises:
        ValueError
    """
    if nb_iter > 0:
        return nb_iter
    else:
        raise ValueError("Number of iterations must be a positive value")


def predict(model, img):
    """ Donne la classe prédite par le modèle pour une image donne
    la classe prédite est celle qui a la plus forte activation
    Args:
        model = keras.Model
        img = numpy image
    Returns:
        dict qui contient la classe pour 'indice'
        et toutes les valeurs de sortie pour 'values'
    """
    x = np.array([img])
    result = model.predict(x)[0]
    m = max(result)
    for i in range(len(result)):
        if result[i] == m:
            return {'class':i, 'values':result}


def get_model_json(model):
    """ Renvoie une string qui correspond à un .json contenant
    pour chaque layer:
        class_name: le nom de la classe keras du layer
        name: le nom du layer
        shape: les dimension du layer
    Args:
        model = keras.Model
    Returns:
        jsonarray = string
    """
    list_layer = list()
    for i in range (0,len(model.layers)):
        if isinstance(model, Sequential):
            class_name = model.get_config()[i]["class_name"]
        else :
            class_name = model.get_config()['layers'][i]["class_name"]
        if ( str(model.layers[i].output_shape[0]) == 'None'):
            if(len(model.layers[i].output_shape)-1 == 1):
                shape = str(model.layers[i].output_shape[1])
            else :
                shape = str(model.layers[i].output_shape[1:])
        else :
            shape = str(model.layers[i].output_shape)
        list_layer.append({"name" : str(model.layers[i].name), "class_name" : class_name, "shape" : shape})
    return json.dumps(list_layer)
