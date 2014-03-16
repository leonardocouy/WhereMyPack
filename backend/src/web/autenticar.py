# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import users
from tekton import router

usuario = users.get_current_user()

def user(_json):
    nome_google = {'nome' : users.get_current_user().nickname()}
    _json(nome_google, '')

def index(_handler, _req):

    if usuario:
       # url = router.to_path('/')
        _handler.redirect('/')
    else:
        _handler.redirect(users.create_login_url(_req.uri))