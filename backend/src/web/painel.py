# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from google.appengine.api import users
from lib.correio import correio
from tekton import router



class Pacote(ndb.Model):
    cod_rastreio = ndb.StringProperty()
    id_google = ndb.StringProperty()
    nome_google = ndb.StringProperty()
    email = ndb.StringProperty()
    local = ndb.StringProperty()
    encaminhado = ndb.StringProperty()
    data = ndb.StringProperty()
    situacao = ndb.StringProperty()

def salvar(_handler,_resp,cod_rastreio,email):
    user_google = users.get_current_user()
    correio.destinatario = email
    correio.cod_rastreio = cod_rastreio
    status = correio.obter_rastreamento(cod_rastreio)
    if user_google:
        pacote = Pacote(cod_rastreio=cod_rastreio, id_google=user_google.user_id(), nome_google=user_google.nickname(), email=email,
                        local=status['local'],encaminhado=status['encaminhado'],situacao=status['situacao'],data=status['data'])
        pacote.put()
        _handler.redirect('/')
    else:
         _resp.write('Erro: Você não está logado.')

def cad_rastreio(_write_tmpl):
    path = router.to_path(salvar)
    dct = {'salvar_rastreio': path}
    _write_tmpl('/templates/painel_cadastrar.html', dct)

def index(_write_tmpl):
    _write_tmpl('templates/painel_index.html')

