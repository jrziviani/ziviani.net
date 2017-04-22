# -*- coding: utf-8 -*-
# templates.py - handles template creation and queries
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
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import TemplateNotFound
from lxml import html

import os


# --
# CONSTANTS
# --
TEMPLATE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'templates')


# --
# IMPLEMENTATION
# --
class templates(object):
    '''
    Implements the template model responsible to assembly the page and returns
    a rendered (MIME) content.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._jinja = Environment(loader=FileSystemLoader(TEMPLATE_DIR),
                                  autoescape=True)

    def get_template(self, name, **context):
        '''
        Returns the rendered content given the template name and the data
        associate to it
        '''
        try:
            template = self._jinja.get_template(name)

        except TemplateNotFound:
            return None

        return template.render(context)

    def get_metatemplate(self):
        '''
        '''
        metadata = []
        article = None
        try:
            with open(os.path.join(TEMPLATE_DIR, 'articles.tmpl')) as article_file:
                article = article_file.read()

        # if it catches any exception something really bad happened
        except:
            return None

        parser = html.fromstring(article)
        posts = parser.xpath('//a[@class="posts"]')

        for post in posts:
            path = post.get('href').split('/')
            metadata.append({'title': post.text,
                             'resume': '',
                             'doc': post.get('data-doc'),
                             'year': path[1],
                             'path': path[2]})
        return metadata

# class Templates
