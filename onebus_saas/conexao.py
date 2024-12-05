# conexao.py
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente do arquivo .env na raiz do projeto
load_dotenv()  # Assumindo que o arquivo .env está na raiz do projeto

class Conexao:
    def __init__(self):
        self.host = os.getenv('ENDPOINT_BANCO')
        self.username = os.getenv('USERNAME_BANCO')
        self.password = os.getenv('PASSWORD_BANCO')
        self.db_name = os.getenv('DB_NAME_BANCO')

    def criar_conexao(self):
        try:
            con = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.db_name,
                charset='utf8'  # Define o charset para evitar problemas de codificação
            )
            if con.is_connected():
                return con
        except Error as e:
            print(f"Erro de conexão: {e}")
            return None
