import sqlite3

#onstante com o nome do banco, caso precise mudar o nome do banco, mudo só aqui
NOME_BANCO = "porta_prego.db"

def conectar_banco():
    """Cria conexão com o arquivo do banco de dados"""
    return sqlite3.connect(NOME_BANCO)

def inicializar_banco():
    """Cria a tabela se ela ainda não existir"""
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS despesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            categoria TEXT)""")


    conexao.commit()
    conexao.close()
    print("Banco de Dados e tabela incializados com sucesso")

def salvar_despesa(data, descricao, valor, categoria):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO despesas (data, descricao, valor, categoria)
        VALUES (?, ?, ?, ?)
    """, data, descricao, valor, categoria)

    conexao.commit()
    conexao.close()

if __name__ =="__main__":
    inicializar_banco()