# -*- coding: utf-8 -*-
# main.wsgi - creates the wsgi application and start it.
# Copyright (C) 2017 Jose Ricardo Ziviani
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# --
# IMPORTS
# --
import os
import sys

sys.path.insert(0, '/var/www/html/')

from src.blog import Blog
from werkzeug.wsgi import SharedDataMiddleware


# --
# CONSTANTS
# --


# --
# IMPLEMENTATION
# --
def deploy():
    app = Blog()
    app.wsgi_app = SharedDataMiddleware(
        app.wsgi_app,
        {
            '/ui/': os.path.join(
                os.path.dirname(__file__), 'ui'),
            '/robots.txt': os.path.join(
                os.path.dirname(__file__), 'robots.txt'),
            '/favicon.ico': os.path.join(
                os.path.dirname(__file__), 'favicon.ico'),
        },
        cache=False,
        cache_timeout=36288000
    )
    return app
# deploy()

application = deploy()

# vim: ft=python:
