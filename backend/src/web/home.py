# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import users


def index(_write_tmpl):
    usuario = users.get_current_user()
    # dict_status = {'usuario': usuario}
    if usuario:
        _write_tmpl('templates/base.html')
    else:
        _write_tmpl('templates/splash.html')
