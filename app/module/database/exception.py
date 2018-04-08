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

class UserNotFoundError( FileNotFoundError ):
    def _init_(self, user):
        msg = "UserNotFoundError: User " + user + " not found"
        super(UserNotFoundError, self).__init__(msg)
        self.user = user

class ModelNotFoundError( FileNotFoundError ):
    def _init_(self, user, model_name):
        msg = "ModelNotFoundError: model " + model + " not found"
        super(ModelNotFoundError, self).__init__(msg)
        self.user = user
        self.model_name = model_name

class VisuNotFoundError( FileNotFoundError ):
    def _init_(self, user, model_name, img_name):
        msg = "VisuNotFoundError: visualization "+ img_name + " not found"
        super(VisuNotFoundError, self).__init__(msg)
        self.user = user
        self.model_name = model_name
        self.img_name = img_name
