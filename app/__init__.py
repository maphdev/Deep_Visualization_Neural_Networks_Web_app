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

### initializes the application and brings together all of the various components.

# import flask and template operators
from flask import Flask, render_template, request

# import WSGI application object
# with instance relative config
app = Flask(__name__, instance_relative_config=True)

# configuration
app.config.from_object("config")
app.config.from_pyfile('config.py')
app.secret_key = "my_secret_key"

# HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', err="Page Not Found", message="The page you are looking for doesn't exist."), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', err="Internal Server Error", message="Sorry for this error, please try again."), 500

@app.errorhandler(Exception)
def unhandled_exception(e):
    return render_template('error.html', err="Unhandled Exception", message="Sorry for this error, please try again."), 500

# import routes
from . import views
