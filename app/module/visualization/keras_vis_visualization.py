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

from .visualization import Maxout, Reason

from keras import activations
from keras.layers.convolutional import _Conv
from keras.layers.pooling import _Pooling1D, _Pooling2D, _Pooling3D
from keras import backend as K

from vis.visualization import visualize_cam, visualize_activation, overlay
from vis.input_modifiers import Jitter
from vis.utils import utils

import sys
import numpy as np

# Visualisation MaxOut
class MaxoutKerasVis( Maxout ):
    def __init__(self):
        pass
    def apply(self, model, layer, filter, nb_iter):
        # Changer l'activation softmax par linear
        model.layers[layer].activation = activations.linear
        model = utils.apply_modifications(model)

        img = visualize_activation(model, layer, filter_indices=filter, max_iter=nb_iter, tv_weight=1., lp_norm_weight=0., verbose=True, input_modifiers=[Jitter(16)])
        if img.shape[2] == 1:
            image = np.zeros(shape=(int(img.shape[0]),int(img.shape[1]), 3))
            for i in range(len(image)):
                for j in range(len(image[i])):
                    image[i][j][0] = img[i][j][0]
                    image[i][j][1] = img[i][j][0]
                    image[i][j][2] = img[i][j][0]
            img = image
        return img

class ReasonKerasVis( Reason ):
    def __init__(self):
        pass
    def apply(self, model, image, layer, filter):
        # Changer l'activation softmax par linear
        model.layers[layer].activation = activations.linear
        model = utils.apply_modifications(model)
        penultimate_layer_idx = None
        if layer == 2 and isinstance(model.layers[1], (_Conv, _Pooling1D, _Pooling2D, _Pooling3D)):
            penultimate_layer_idx = 1
        elif layer <= 2 and isinstance(model.layers[0], (_Conv, _Pooling1D, _Pooling2D, _Pooling3D)):
            penultimate_layer_idx = 0
        grads = visualize_cam(model, layer, filter_indices=filter, backprop_modifier="guided", grad_modifier=None, seed_input=image, penultimate_layer_idx=penultimate_layer_idx)
        shape = model.layers[0].input_shape
        if shape[len(shape)-1] == 1:
            img = None
            if K.image_data_format() == 'channels_first':
                img = np.zeros(shape=(int(model.input.shape[2]),int(model.input.shape[3]), 3))
            else:
                img = np.zeros(shape=(int(model.input.shape[1]),int(model.input.shape[2]), 3))
            for i in range(len(image)):
                for j in range(len(image[i])):
                    img[i][j][0] = image[i][j][0]
                    img[i][j][1] = image[i][j][0]
                    img[i][j][2] = image[i][j][0]
            image = img
        grads = overlay(grads, image)
        return grads
