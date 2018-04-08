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

class Visualization( object ):
    """An Abstract class for vizualisation to specify some interface."""

class Maxout( Visualization ):
    """An Abstract class for vizualisation Maxout to specify some interface."""
    def apply(self, model, layer, filter, nb_iter):
        """ Ranvoie visualisation Maxout
        Attention ne vérifie pas la validité des arguments passés en paramètre
        Args:
            model = keras.model
            layer = (int) in range(len(model.layers))
            filter = (int) in range(len(get_num_filters(layer)))
            nb_iter = (int) nombre d'itération
        Returns:
            numpy image
        """
        raise NotImplementedError( "Should be implemented" )

class Reason( Visualization ):
    """An Abstract class for vizualisation Reason to specify some interface."""
    def apply(self, model, image, layer, filter):
        """ Ranvoie visualisation Reason pour une unité donné
        Attention ne vérifie pas la validité des arguments passés en paramètre
        Args:
            model = keras.model
            image = numpy image
            layer = (int) in range(len(model.layers))
            filter = (int) in range(len(get_num_filters(layer)))
        Returns:
            numpy image
        Raises:
            ValueError
        """
        raise NotImplementedError( "Should be implemented" )
