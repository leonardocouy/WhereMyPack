# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb, deferred
from google.appengine.api import users, taskqueue
from lib.correio import correio
from tekton import router
from web.autentifer import usuariogoogle


user_google = users.get_current_user()
dict_google = {'user_google': user_google.nickname()}


class Pacote(ndb.Model):
    cod_rastreio = ndb.StringProperty()
    nome_google = ndb.StringProperty()
    email = ndb.StringProperty()
    local = ndb.StringProperty()
    encaminhado = ndb.StringProperty()
    data = ndb.StringProperty()
    situacao = ndb.StringProperty()


def extrai_infos(cod_rastreio):
    source_html = correio.captura_html(
        'http://websro.correios.com.br/sro_bin/txect01$.QueryList?P_ITEMCODE=&P_LINGUA=001&P_TESTE=&P_TIPO=001&P_COD_UNI=%s' % cod_rastreio)
    status = correio.extracao(source_html)
    return status


def verificar_status():
    allregisters = Pacote.query()
    for reg_sel in allregisters.fetch():
        infos = reg_sel.to_dict()
        correio.destinatario = infos['email']
        correio.cod_rastreio = infos['cod_rastreio']
        status = extrai_infos(infos['cod_rastreio'])

        pacote = Pacote(cod_rastreio=infos['cod_rastreio'],
                        email=infos['email'],
                        local=status['local'], encaminhado=status['encaminhado'], situacao=status['situacao'],
                        data=status['data'], nome_google=infos['nome_google'])

        query = Pacote.query().filter(Pacote.data == status['data']).filter(
            Pacote.nome_google == users.get_current_user().nickname()).filter(
            Pacote.cod_rastreio == status['codigorast'])
        datadb = {'data': '00/00/0000', 'situacao': 'nada'}

        for c in query.fetch():
            datadb = c.to_dict()

        if datadb['data'] != status['data']:
            pacote.put()
            correio.email(status, reg_sel.email)


def salvar(_write_tmpl, cod_rastreio, email):
    correio.destinatario = email
    correio.cod_rastreio = cod_rastreio
    status = extrai_infos(cod_rastreio)
    if status == {}:
        errodict = {'erro': 'Este código não existe, ou não possui registros ainda.'}
        _write_tmpl('/templates/painel_erros.html', errodict)
    else:
        query = Pacote.query().filter(Pacote.data == status['data']).filter(
        Pacote.nome_google == users.get_current_user().nickname()).filter(Pacote.cod_rastreio == status['codigorast'])
        pacote = Pacote(cod_rastreio=cod_rastreio,
                        email=email,
                        local=status['local'], encaminhado=status['encaminhado'], situacao=status['situacao'],
                        data=status['data'], nome_google=usuariogoogle.nickname())
        datadb = {'data': '00/00/0000'}
        for c in query.fetch():
            datadb = c.to_dict()

        if datadb['data'] != status['data']:
            pacote.put()
            correio.email(status, email)
            errodict = {'erro': 'Código cadastrado com sucesso no sistema'}
            _write_tmpl('/templates/painel_erros.html', errodict)
        else:
            errodict = {'erro': 'Este código já esta cadastrado no seu usuario.'}
            _write_tmpl('/templates/painel_erros.html', errodict)


def cad_rastreio(_write_tmpl):
    path = router.to_path(salvar)
    dct = {'salvar_rastreio': path}
    _write_tmpl('/templates/painel_cadastrar.html', dct)


def listar_codigos(_json):
    query = Pacote.query().filter(Pacote.nome_google == users.get_current_user().nickname())
    listinha = []
    for x in query.fetch():
        datadb = x.to_dict()
        listinha.append(datadb['cod_rastreio'])
    listinha2 = list(set(listinha))
    _json(listinha2, '')


def listar_rastreio(_json, _write_tmpl, cod_rastreio):
    query = Pacote.query().filter(Pacote.nome_google == usuariogoogle.nickname()).filter(
        Pacote.cod_rastreio == cod_rastreio)
    query = query.order(-Pacote.data)
    encomendas = query.fetch()
    encomendas_dct = [p.to_dict() for p in encomendas]
    if encomendas == []:
        errodict = {'erro': 'Você não possui encomenda cadastrada!'}
        _write_tmpl('/templates/painel_erros.html', errodict)
    else:
        _json(encomendas_dct, '')


def listar(_write_tmpl):
    query = Pacote.query().filter(Pacote.nome_google == usuariogoogle.nickname())
    verificar_encomendas = query.fetch()
    if verificar_encomendas == []:
        errodict = {'erro': 'Você não possui encomenda cadastrada!'}
        _write_tmpl('/templates/painel_erros.html', errodict)
    else:
        _write_tmpl('/templates/painel_listar.html')


def index(_write_tmpl):
    _write_tmpl('templates/painel_index.html')

