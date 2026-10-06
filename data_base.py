import os
import sqlite3
import psycopg2

#Verifica se a Render forenceu uma instância Postgresql
#Se não foi encontrada ele usa o Sqlite

DATABASE_URL = os.environ.get("DATABASE_URL")

def conectar_banco():
    """ Cria a conexão corrreta de onde o código está rodando"""

    if DATABASE_URL:
        #Conecta o Postgre na nuvem
        return psycopg2.connect(DATABASE_URL)
    else:
        #Cria a conexão com o Sqlite
        conexao = conectar_banco()
        cursor = conexao.cursor()
    #O comando SQL muda de INREGER para SERIAL no Postgre
    if DATABASE_URL:
        #criação da tabela no Postgre
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS despesas (
                id SERIAL PRIMARY KEY,
                data TEXT NOT NULL,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                categoria TEXT
            )
        """)
    else:
        #criação da tabela no Sqlite
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS despesas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                categoria TEXT
            )
        """)

    conexao.commit()
    conexao.close()
    print("🗄️ Banco de dados inicializado com sucesso!")

def salvar_despesa(data, descricao, valor, categoria):
    """Insere um novo gasto"""
    conexao = conectar_banco()
    cursor = conexao.cursor()

    #O insert funciona da mesma forma nos dois bancos
    cursor.execute("""
        INSERT INTO despesas (data, descricao, valor, categoria) 
        VALUES (?,?,?,?)"""
                   .replace("?", "%S" if DATABASE_URL else "?"), (data, descricao, valor, categoria))
    #O postgre usa "%s" no lugar de "?"

    conexao.commit()
    conexao.close()

