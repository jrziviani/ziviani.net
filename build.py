#!/usr/bin/env python2.7
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
from src.templates import templates

import os
import sys
import subprocess


# --
# CONSTANTS
# --
DEFAULT_DIR = os.path.dirname(os.path.realpath(__file__))


# --
# IMPLEMENTATION
# --
def run_command(cmd):
    '''
    Runs arbitrary command on shell
    '''
    proc = subprocess.Popen(cmd.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    out, err = proc.communicate()
    if err:
        print err
        #sys.exit(1)

    return out

def create_feeds():
    '''
    Creates the feed.xml file based on the published posts available
    '''
    print 'Creating feeds'
    tmpls = templates()
    if not tmpls.generate_metadata():
        print 'ERROR: cannot create feed.xml'
        sys.exit(1)

def update_folder():
    '''
    Updates local repository
    '''
    print 'Updating folders'
    run_command('git pull')


# --
# ENTRY POINT
# --
if __name__ == '__main__':
    update_folder()
    create_feeds()
