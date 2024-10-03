import mysql.connector
from mysql.connector import Error

class Conexao:

    def criar_conexao(self):
        try:
            host = "onebus.cx8kmic8cryz.us-east-2.rds.amazonaws.com"
            username = "admin"
            password = "onebus123"
            db_name = "onebus"

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
