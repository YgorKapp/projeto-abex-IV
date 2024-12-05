# db.py
from flask_mysqldb import MySQL
from flask import Flask
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente a partir do arquivo .env
load_dotenv('/home/ixcsoft/Documentos/onebus/projeto-abex-IV/.env')

def init_db(app: Flask):
    app.config['MYSQL_HOST'] = os.getenv('ENDPOINT_BANCO')
    app.config['MYSQL_USER'] = os.getenv('USERNAME_BANCO')
    app.config['MYSQL_PASSWORD'] = os.getenv('PASSWORD_BANCO')
    app.config['MYSQL_DB'] = os.getenv('DB_NAME_BANCO')
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Opcional: para retornar resultados como dicionários

    mysql = MySQL(app)
    return mysql
