# -*- coding: utf-8 -*-

from google.appengine.ext import ndb
from google.appengine.api import users
from tekton import router



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

def index(_resp,_req):
    _resp.write("Pagina do Usuário")
    _resp.write(" Cookies: %s" % _req.cookies)


def ola(_resp):
    _resp.write("Olá")


def calculadora(_resp, operacao, num1, num2):
    if (operacao == '-'):
        total = int(num2) - int(num1)
        _resp.write("O Resultado é: %s" % total)
    elif (operacao == '+'):
        total = int(num1) + int(num2)
        _resp.write("O Resultado é: %s" % total)
    elif (operacao == '*'):
        total = int(num1) * int(num2)
        _resp.write("O Resultado é: %s" % total)
    elif (operacao == '/'):
        total = int(num1) / int(num2)
        _resp.write("O Resultado é: %s" % total)
    else:
        _resp.write("Operação invalida!!!!!")


def redirecionar(_handler):
    url = str('http://google.com.br')
    _handler.redirect(url)

def principal(_handler,_req):
    usuario = users.get_current_user()
    #usuario.nickname;
    if usuario:
        url = router.to_path(calculadora, '+', '5', '20')
        _handler.redirect(url)
    else:
        _handler.redirect(users.create_login_url(_req.uri))