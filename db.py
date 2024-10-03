from flask import Flask, jsonify
from flask_mysqldb import MySQL

def init_db(app: Flask):
    app.config['MYSQL_HOST'] = 'onebus.cx8kmic8cryz.us-east-2.rds.amazonaws.com'
    app.config['MYSQL_USER'] = 'admin'
    app.config['MYSQL_PASSWORD'] = 'onebus123'
    app.config['MYSQL_DB'] = 'onebus'

    mysql = MySQL(app)
    return mysql

def inserir_banco(query, usuario):
    # Inserir no banco de dados
    try:
        cursor = MySQL.connection.cursor()
        cursor.execute(query, (usuario.nome, usuario.username, usuario.email, usuario.telefone, usuario.senha))

        MySQL.connection.commit()
        cursor.close()

        return jsonify({'message': 'Usuário registrado com sucesso!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500