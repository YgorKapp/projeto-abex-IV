# app.py
from flask import Flask, render_template, request, redirect, session, flash, url_for
from classes.Usuario import Usuario
from db import init_db
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb.cursors
from conexao import Conexao
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'onebus')  # Utilize uma chave secreta mais segura em produção

# Inicializa o MySQL
mysql = init_db(app)

# Decorador para proteger rotas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('acessarconta'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html', title='One Bus', back_style='body-intro')

# Rotas de cadastro
@app.route('/cadastro/<string:tipo>')
def cadastro(tipo):
    
    if tipo == 'criarconta':
        return render_template('criarconta.html', title='Cadastre-se', back_style='body-background')
    if tipo == 'trajetos':
        return render_template('cadastrotrajetos.html', title='Cadastro de trajetos', back_style='body-background')
    if tipo == 'pontos':
        return render_template('cadastrarpontos.html', title='Cadastro de pontos', back_style='body-background')
    if tipo == 'onibus':
        return render_template('cadastroonibus.html', title='Cadastro de onibus', back_style='body-background')
    if tipo == 'motorista':
        return render_template('cadastrarmotorista.html', title='Cadastro de motorista', back_style='body-background')
    # Adicione outras rotas de cadastro conforme necessário
    else:
        return "Tipo de cadastro inválido", 404

# Rota de termos e condições
@app.route('/aceite')
def aceite():
    return render_template('aceitartermos.html', title='Termos de uso', back_style='body-background')

# Rota de acesso à conta (login)
@app.route('/acessarconta')
def acessarconta():
    return render_template('acessarconta.html', title='Entrar', back_style='body-background')

# Rota home (protegida)

# Rota de paradas (protegida)

# Rota de trajetos (protegida)

# Autenticação de usuário (login)
from flask import flash, redirect, url_for, session, request
from werkzeug.security import check_password_hash

@app.route('/autenticar', methods=['POST'])
def autenticar():
    # Obter dados do formulário de login
    username = request.form.get('username')
    senha = request.form.get('senha')

    # Validação básica
    if not username or not senha:
        flash('Por favor, preencha ambos os campos de login e senha.', 'danger')
        return redirect(url_for('acessarconta'))

    try:
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM T_USUARIOS WHERE USERNAME = %s OR EMAIL = %s"
        cursor.execute(query, (username, username))
        user = cursor.fetchone()
        cursor.close()
        
        print("user")  # Verifique o retorno do banco de dados
        print(user)  # Verifique o retorno do banco de dados

        if not user:
            flash('Usuário não encontrado.', 'danger')
            return redirect(url_for('acessarconta'))

        # Validar senha
        if check_password_hash(user['SENHA'], senha):
            # Login bem-sucedido
            print('login ok')
            session['loggedin'] = True
            print(session['loggedin'])
            session['id'] = user['ID']
            session['username'] = user['USERNAME']
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('home'))
        else:
            # Senha incorreta
            flash('Senha incorreta. Por favor, tente novamente.', 'danger')
            print('login não ok')
            return redirect(url_for('acessarconta'))
    
    except Exception as e:
        flash(f'Ocorreu um erro durante a autenticação: {str(e)}', 'danger')
        return redirect(url_for('acessarconta'))

# Registro de usuário
@app.route('/registrar/<string:tipo>', methods=['POST', 'GET'])
def registrar(tipo):
    if tipo == 'usuario' and request.method == 'POST':
        
        # Obter dados do formulário
        nome = request.form.get('nome')
        username = request.form.get('username')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        senha = request.form.get('senha')
        conferesenha = request.form.get('conferesenha')

        # Validação básica
        if not nome or not username or not email or not senha:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return redirect(url_for('cadastro', tipo='criarconta'))

        # Verificar se as senhas correspondem
        if senha != conferesenha:
            flash('As senhas não correspondem.', 'danger')
            return redirect(url_for('cadastro', tipo='criarconta'))

        # Hash da senha
        senha_hash = generate_password_hash(senha)

        try:
            cursor = mysql.connection.cursor()
            query = """
                INSERT INTO T_USUARIOS (NOME, USERNAME, EMAIL, TELEFONE, SENHA)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nome, username, email, telefone, senha_hash))
            mysql.connection.commit()
            cursor.close()

            flash('Usuário registrado com sucesso!', 'success')
            return redirect(url_for('acessarconta'))
        except MySQLdb.IntegrityError as e:
            # Verifica se é erro de duplicidade (username ou email)
            if 'Duplicate entry' in str(e):
                flash('Username ou Email já estão em uso.', 'danger')
            else:
                flash('Ocorreu um erro durante o registro. Tente novamente.', 'danger')
            return redirect(url_for('cadastro', tipo='criarconta'))
        except Exception as e:
            flash(f'Ocorreu um erro: {str(e)}', 'danger')
            return redirect(url_for('cadastro', tipo='criarconta'))
    
    if tipo == 'usuario' and request.method == 'GET':
        return redirect(url_for('cadastro', tipo='criarconta'))

    elif tipo == 'motorista' and request.method == 'POST':
        
        # Obter dados do formulário
        nome_motorista = request.form.get('nome_motorista')
        cpf_motorista = request.form.get('cpf_motorista')
        chassi_onibus = request.form.get('chassi_onibus')

        # Validação básica
        if not nome_motorista or not cpf_motorista or not chassi_onibus:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return redirect(url_for('cadastro', tipo='motorista'))

        try:
            cursor = mysql.connection.cursor()
            query = """
                INSERT INTO T_MOTORISTAS (NOME_MOTORISTA, CPF_MOTORISTA, CHASSI_ONIBUS)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (nome_motorista, cpf_motorista, chassi_onibus))
            mysql.connection.commit()
            cursor.close()

            flash('Motorista registrado com sucesso!', 'success')
            return redirect(url_for('home'))  # Redireciona para a página inicial ou outra página relevante
        except MySQLdb.IntegrityError as e:
            # Verifica se há erro de duplicidade, como CPF
            if 'Duplicate entry' in str(e):
                flash('Este CPF já está registrado.', 'danger')
            else:
                flash('Ocorreu um erro durante o registro. Tente novamente.', 'danger')
            return redirect(url_for('cadastro', tipo='motorista'))
        except Exception as e:
            flash(f'Ocorreu um erro: {str(e)}', 'danger')
            return redirect(url_for('cadastro', tipo='motorista'))
    
    if tipo == 'motorista' and request.method == 'GET':
        return redirect(url_for('cadastro', tipo='motorista'))

    elif tipo == 'onibus' and request.method == 'POST':
        
        # Obter dados do formulário
        modelo_onibus = request.form.get('modelo_onibus')
        placa_onibus = request.form.get('placa')
        chassi_onibus = request.form.get('chassi')
        capacidade_onibus = request.form.get('capacidade')

        # Validação básica
        if not modelo_onibus or not placa_onibus or not chassi_onibus or not capacidade_onibus:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return redirect(url_for('cadastro', tipo='motorista'))

        try:
            cursor = mysql.connection.cursor()
            query = """
                INSERT INTO T_ONIBUS (ONI_MODELO, ONI_PLACA, ONI_CHASSI, ONI_CAPACIDADE, ONI_ID_APLICATIVO)
                VALUES (%s, %s, %s, %s, 1)
            """
            cursor.execute(query, (modelo_onibus, placa_onibus, chassi_onibus, capacidade_onibus))
            mysql.connection.commit()
            cursor.close()

            flash('Ônibus registrado com sucesso!', 'success')
            return redirect(url_for('home'))  # Redireciona para a página inicial ou outra página relevante
        except MySQLdb.IntegrityError as e:
            # Verifica se há erro de duplicidade, como CPF
            if 'Duplicate entry' in str(e):
                flash('Este ônibus já está registrado.', 'danger')
            else:
                flash('Ocorreu um erro durante o registro. Tente novamente.', 'danger')
            return redirect(url_for('cadastro', tipo='motorista'))
        except Exception as e:
            flash(f'Ocorreu um erro: {str(e)}', 'danger')
            return redirect(url_for('cadastro', tipo='motorista'))
    
    if tipo == 'onibus' and request.method == 'GET':
        return redirect(url_for('cadastro', tipo='onibus'))

    elif tipo == 'ponto' and request.method == 'POST':
        
        # Obter dados do formulário
        descricao_ponto = request.form.get('descricao_ponto')
        latitude = float(request.form.get('latitude'))
        longitude = float(request.form.get('longitude'))

        print(latitude)
        print(longitude)
        # Validação básica
        if not descricao_ponto or not latitude or not longitude:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return redirect(url_for('cadastro', tipo='motorista'))

        try:
            cursor = mysql.connection.cursor()
            query = """
                INSERT INTO T_PONTOS (PON_DESCRICAO, PON_LATITUDE, PON_LONGITUDE)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (descricao_ponto, latitude, longitude))
            mysql.connection.commit()
            cursor.close()

            flash('Ponto registrado com sucesso!', 'success')
            return redirect(url_for('home'))  # Redireciona para a página inicial ou outra página relevante
        except MySQLdb.IntegrityError as e:
            # Verifica se há erro de duplicidade, como CPF
            if 'Duplicate entry' in str(e):
                flash('Este ponto já está registrado.', 'danger')
            else:
                flash('Ocorreu um erro durante o registro. Tente novamente.', 'danger')
            return redirect(url_for('cadastro', tipo='motorista'))
        except Exception as e:
            flash(f'Ocorreu um erro: {str(e)}', 'danger')
            return redirect(url_for('cadastro', tipo='motorista'))
    
    elif tipo == 'ponto' and request.method == 'GET':
            return redirect(url_for('cadastro', tipo='pontos'))

    elif tipo == 'trajeto' and request.method == 'POST':
        
        # Obter dados do formulário
        descricao_ponto = request.form.get('descricao_ponto')
        latitude = float(request.form.get('latitude'))
        longitude = float(request.form.get('longitude'))


        # Validação básica
        if not descricao_ponto or not latitude or not longitude:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return redirect(url_for('cadastro', tipo='motorista'))

        try:
            cursor = mysql.connection.cursor()
            query = """
                INSERT INTO T_PONTOS (PON_DESCRICAO, PON_LATITUDE, PON_LONGITUDE)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (descricao_ponto, latitude, longitude))
            mysql.connection.commit()
            cursor.close()

            flash('Ponto registrado com sucesso!', 'success')
            return redirect(url_for('home'))  # Redireciona para a página inicial ou outra página relevante
        except MySQLdb.IntegrityError as e:
            # Verifica se há erro de duplicidade, como CPF
            if 'Duplicate entry' in str(e):
                flash('Este ponto já está registrado.', 'danger')
            else:
                flash('Ocorreu um erro durante o registro. Tente novamente.', 'danger')
            return redirect(url_for('cadastro', tipo='motorista'))
        except Exception as e:
            flash(f'Ocorreu um erro: {str(e)}', 'danger')
            return redirect(url_for('cadastro', tipo='motorista'))
    
    if tipo == 'trajeto' and request.method == 'GET':
        return redirect(url_for('cadastro', tipo='trajeto'))
        

    else:
        flash('Tipo de registro inválido.', 'danger')
        return redirect(url_for('home'))

# Logout de usuário

if __name__ == '__main__':
    app.run(debug=True)
