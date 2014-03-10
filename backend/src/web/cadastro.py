# -*- coding: utf-8 -*-

from google.appengine.ext import ndb


def index(_write_tmpl):
    class Pessoa(ndb.Model):
        nome=ndb.StringProperty()
        idade=ndb.IntegerProperty()

    def cadastro(nome,idade):
        idade = int(idade)
        salvar = Pessoa(nome=nome, idade=idade)
        salvar.put()

    def mostrar(_resp):
        query = Pessoa.query()
        for c in query.fetch():
            lista_pessoa = c.to_dict()
        _resp.write(lista_pessoa)

