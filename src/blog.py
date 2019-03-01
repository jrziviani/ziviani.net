# -*- coding: utf-8 -*-
# blog.py - maps requests to methods and handles them accordingly.
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
from werkzeug.routing import Map
from werkzeug.routing import Rule
from werkzeug.wrappers import Request
from werkzeug.wrappers import Response
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import HTTPException
from werkzeug.utils import redirect
from werkzeug.urls import url_fix
from templates import templates

import logging
import hashlib
import re


# --
# CONSTANTS
# --


# --
# IMPLEMENTATION
# --
class Blog(object):
    '''
    Implements the ziviani.net controller
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._urls = Map([
            Rule('/', endpoint='index'),
            Rule('/ptbr', endpoint='ptbr_index'),
            Rule('/feed', endpoint='feed'),
            Rule('/about', endpoint='about'),
            Rule('/ptbr/about', endpoint='ptbr_about'),
            Rule('/articles', endpoint='articles'),
            Rule('/ptbr/articles', endpoint='ptbr_articles'),
            Rule('/links', endpoint='hotlinks'),
            Rule('/ptbr/links', endpoint='ptbr_hotlinks'),
            #Rule('/resume', endpoint='resume'),
            Rule('/<int:year>/<page>', endpoint='posts'),
            Rule('/<int:year>/ptbr/<page>', endpoint='ptbr_posts'),
            Rule('/search', endpoint='search'),
        ])

        logging.basicConfig()
        self._logger = logging.getLogger('[ BLOG ]')
        self._logger.setLevel(logging.ERROR)
        self._templates = templates()

    def _on_index(self, request):
        '''
        Handles the main page request
        '''
        return self._on_posts(request, '2019', 'amps-template-engine')

    def _on_ptbr_index(self, request):
        '''
        Handles the main page request
        '''
        return self._on_ptbr_posts(request, '2017', 'funcoes-em-assembly')

    def _on_feed(self, request):
        '''
        Handles the feed (rss) request
        '''
        response = self._templates.get_feed()
        if response is None:
            self._logger.error('feed not found, missed generate_metadata?')
            raise NotFound()
        return Response(response, mimetype='application/rss+xml')

    def _on_posts(self, request, year, page):
        '''
        Handles requests to posts
        '''
        page_data = {}
        page_data['url'] = 'https://ziviani.net/%s/%s' % (year, page)
        page_data['uid'] = hashlib.md5(page_data['url']).hexdigest()

        response = self._templates.get_template("%s.tmpl" % page, data=page_data)
        if response is None:
            self._logger.error('template %s not found', page)
            raise NotFound()

        return Response(response, mimetype='text/html')

    def _on_ptbr_posts(self, request, year, page):
        '''
        Handles requests to posts in brazilian portuguese
        '''
        page_data = {}
        page_data['url'] = 'https://ziviani.net/%s/ptbr/%s/' % (year, page)
        page_data['uid'] = hashlib.md5(page_data['url']).hexdigest()

        response = self._templates.get_template("ptbr/%s.tmpl" % page, data=page_data)
        if response is None:
            self._logger.error('template ptbr/%s not found', page)
            raise NotFound()

        return Response(response, mimetype='text/html')

    def _on_articles(self, request):
        '''
        Handles request to articles page
        '''
        response = self._templates.get_template("article.tmpl")
        return Response(response, mimetype='text/html')

    def _on_ptbr_articles(self, request):
        '''
        Handles request to articles page
        '''
        response = self._templates.get_template("ptbr/article.tmpl")
        return Response(response, mimetype='text/html')

    def _on_hotlinks(self, request):
        '''
        Handles request to link page
        '''
        response = self._templates.get_template("hotlinks-v1.tmpl")
        return Response(response, mimetype='text/html')

    def _on_ptbr_hotlinks(self, request):
        '''
        Handles request to link page
        '''
        response = self._templates.get_template("ptbr/hotlinks-v1.tmpl")
        return Response(response, mimetype='text/html')

    def _on_about(self, request):
        '''
        Handles requests to About page
        '''
        response = self._templates.get_template("about.tmpl")
        return Response(response, mimetype='text/html')

    def _on_ptbr_about(self, request):
        '''
        Handles requests to About page
        '''
        response = self._templates.get_template("ptbr/about.tmpl")
        return Response(response, mimetype='text/html')

    def _on_resume(self, request):
        '''
        Handles resume page
        '''
        response = self._templates.get_template("resume.tmpl")
        return Response(response, mimetype='text/html')

    def _on_search(self, request):
        '''
        Handles internal searches using DuckDuckGo
        '''
        if request.method != 'POST':
            return self._on_index(request)

        query = re.sub(r'[^0-9A-Za-z-+., ]',
                       r' ',
                       request.form['search'],
                       flags=re.UNICODE)

        if len(query) > 25:
            query = query[:25]

        search_q = 'https://duckduckgo.com/?q=site:ziviani.net %s' % query
        search_q+= '&kae=dark&kj=%23282828&k7=%23383838&k5=1&kx=%23f7ca88'
        search_q+= '&kt=n&k5=1&t=ziviani.net&km=l&kn=0&kae=dark&kh=1&kg=p'

        return redirect(url_fix(search_q))

    def _not_found(self):
        '''
        Handles 404 - page not found!
        '''
        response = self._templates.get_template("notfound.tmpl")
        return Response(response, mimetype='text/html', status=404)

    def _dispatch(self, request):
        '''
        Maps the request to the appropriate method
        '''
        adapter = self._urls.bind_to_environ(request.environ)

        try:
            endpoint, values = adapter.match()
            return getattr(self, '_on_' + endpoint)(request, **values)

        # show the spacial page not found
        except NotFound, e:
            return self._not_found()

        # go back do index if any other isse
        except HTTPException, e:
            self._logger.error(str(e))
            return self._on_index(request)

    def wsgi_app(self, environ, start_response):
        '''
        Abstracts request/response calls in a couple of lines
        '''
        request = Request(environ)
        response = self._dispatch(request)

        return response(environ, start_response)

    def __call__(self, environ, start_response):
        '''
        Main method
        '''
        return self.wsgi_app(environ, start_response)
# class Blog()
