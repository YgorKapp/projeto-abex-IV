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
@app.route('/home')
@login_required
def home():
    return render_template('home.html', title='One Bus', back_style='body-background')

# Rota de paradas (protegida)
@app.route('/paradas')
@login_required
def paradas():
    return render_template('paradas.html', title='Paradas', back_style='body-background')

# Rota de trajetos (protegida)
@app.route('/trajetos')
@login_required
def trajetos():
    return render_template('trajetos.html', title='Trajetos', back_style='body-background')

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
    elif tipo == 'usuario' and request.method == 'GET':
        return redirect(url_for('cadastro', tipo='criarconta'))
    else:
        flash('Tipo de registro inválido.', 'danger')
        return redirect(url_for('home'))

# Logout de usuário
@app.route('/logout')
@login_required
def logout():
    # Limpa a sessão do usuário
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    flash('Você foi desconectado com sucesso.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
