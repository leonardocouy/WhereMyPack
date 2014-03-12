# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from google.appengine.api import users
from lib.correio import correio
from tekton import router
from datetime import datetime


class Pacote(ndb.Model):
    cod_rastreio = ndb.StringProperty()
    id_google = ndb.StringProperty()
    nome_google = ndb.StringProperty()
    email = ndb.StringProperty()
    local = ndb.StringProperty()
    encaminhado = ndb.StringProperty()
    data = ndb.StringProperty()
    situacao = ndb.StringProperty()


def extrai_infos(cod_rastreio):
    source_html = correio.captura_html(
        'http://websro.correios.com.br/sro_bin/txect01$.QueryList?P_ITEMCODE=&P_LINGUA=001&P_TESTE=&P_TIPO=001&P_COD_UNI=%s'%cod_rastreio)
    status = correio.extracao(source_html)
    return status


def salvar(_write_tmpl, _resp, cod_rastreio, email):
    user_google = users.get_current_user()
    correio.destinatario = email
    correio.cod_rastreio = cod_rastreio

    status = extrai_infos(cod_rastreio)
    query = Pacote.query().filter(Pacote.data == status ['data'] and Pacote.cod_rastreio == status ['codigorast'])
    pacote = Pacote(cod_rastreio=cod_rastreio, id_google=user_google.user_id(), nome_google=user_google.nickname(),
                    email=email,
                    local=status['local'], encaminhado=status['encaminhado'], situacao=status['situacao'],
                    data=status['data'])
    datadb = {'data': '00/00/0000'}
    for c in query.fetch():
        datadb = c.to_dict()


    if datadb['data'] != status['data']:
        pacote.put()
        correio.email(status, email)
        _resp.write("Envio sucesso!")
    else:
        _resp.write("Não houve nenhuma alteração no seu rastreio ainda...")
    envio_dict = {"status_envio": correio.message_error}
    #_write_tmpl('templates/painel_index.html', envio_dict)

def cad_rastreio(_write_tmpl):
    path = router.to_path(salvar)
    dct = {'salvar_rastreio': path}
    _write_tmpl('/templates/painel_cadastrar.html', dct)


def index(_write_tmpl):
    _write_tmpl('templates/painel_index.html')

