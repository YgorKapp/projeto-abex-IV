import mysql.connector
from dotenv import dotenv_values
from mysql.connector import Error

config = dotenv_values('/home/ixcsoft/Documentos/onebus/projeto-abex-IV/.env') # Validar endereço

class Conexao:

    def criar_conexao(self):
        try:
            host = config['ENDPOINT_BANCO']
            username = config['USERNAME_BANCO']
            password = config['PASSWORD_BANCO']
            db_name = config['DB_NAME_BANCO']

            con = mysql.connector.connect(
                host=host,
                user=username,
                password=password,
                database=db_name
            )

            if con.is_connected():
                print("Conexão bem-sucedida!")
                con.set_charset_collation('utf8')
                return con

        except Error as e:
            print(f"Erro: {e}")
            return None
