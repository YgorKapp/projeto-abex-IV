from flask import Flask, render_template, request, redirect, session, flash, url_for


app = Flask(__name__)
app.secret_key = 'onebus'
@app.route('/')
def index():
    return render_template('index.html', title='One Bus', back_style='body-intro')

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
    
@app.route('/aceite')
def aceite():
    return render_template('aceitartermos.html', title='Termos de uso', back_style='body-background')

@app.route('/acessarconta')
def acessarconta():
    return render_template('acessarconta.html', title='Entrar', back_style='body-background')

@app.route('/home')
def home():
    return render_template('home.html', title='One Bus', back_style='body-background')

@app.route('/paradas')
def paradas():
    return render_template('paradas.html', title='Paradas', back_style='body-background')

@app.route('/trajetos')
def trajetos():
    return render_template('trajetos.html', title='Trajetos', back_style='body-background')

app.run(debug=True)