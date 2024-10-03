from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from classes.Usuario import Usuario
from classes.Motorista import Motorista
from classes.Onibus import Onibus
# from classes.Ponto import Ponto
from db import *

app = Flask(__name__)
app.secret_key = 'onebus'
@app.route('/')
def index():
    return render_template('index.html', title='One Bus', back_style='body-intro')

# renderizando formularios
@app.route('/cadastro/<string:tipo>')
def cadastro(tipo):
    if tipo == 'criarconta':
        return render_template('criarconta.html', title='Cadastre-se', back_style='body-background')
    elif tipo == 'trajetos':
        return render_template('cadastrotrajetos.html', title='Cadastrar trajeto', back_style='body-background')
    elif tipo == 'pontos':
        return render_template('cadastrarpontos.html', title='Cadastrar pontos', back_style='body-background')
    elif tipo == 'onibus':
        return render_template('cadastroonibus.html', title='Cadastrar ônibus', back_style='body-background')
    elif tipo == 'motorista':
        return render_template('cadastrarmotorista.html', title='Cadastrar motoristas', back_style='body-background')
    else:
        return "Tipo de cadastro inválido", 404

# renderizando termos e condicoes de uso
@app.route('/aceite')
def aceite():
    return render_template('aceitartermos.html', title='Termos de uso', back_style='body-background')

# renderizando tela de boas-vindas
@app.route('/acessarconta')
def acessarconta():
    return render_template('acessarconta.html', title='Entrar', back_style='body-background')

# renderizando home
@app.route('/home')
def home():
    return render_template('home.html', title='One Bus', back_style='body-background')

# renderizando tela de paradas
@app.route('/paradas')
def paradas():
    return render_template('paradas.html', title='Paradas', back_style='body-background')

# renderizando tela de trajetos
@app.route('/trajetos')
def trajetos():
    return render_template('trajetos.html', title='Trajetos', back_style='body-background')

# renderizando tela de login
@app.route('/login')
def login():
    return render_template('login.html', title='Login', back_style='body-background')

# vereficando usuario
@app.route('/autenticar', methods=['POST',])
def autenticar():
    return redirect(url_for('home'))

# interacao com o banco
@app.route('/registrar/<string:tipo>', methods=['POST', 'GET'])
def registrar(tipo):
    if tipo == 'usuario':
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)