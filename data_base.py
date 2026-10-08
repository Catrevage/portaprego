import os
import sqlite3
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")


def conectar_banco():
    """Cria a conexão correta dependendo de onde o código está rodando."""
    if DATABASE_URL:
        return psycopg2.connect(DATABASE_URL)
    else:
        return sqlite3.connect("portaprego.db")


# ====== Cria a tabela se ela não existir ======
def inicializar_banco():
    """Cria a tabela de despesas se ela ainda não existir."""
    conexao = conectar_banco()
    cursor = conexao.cursor()

    # O PostgreSQL usa SERIAL para auto-incremento, o SQLite usa AUTOINCREMENT
    if DATABASE_URL:
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS despesas
                       (
                           id SERIAL PRIMARY KEY,
                           data TEXT NOT NULL,
                           descricao TEXT NOT NULL,
                           valor REAL NOT NULL,
                           categoria TEXT
                       )
                       """)
    else:
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS despesas
                       (
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


# ========================================================

def salvar_despesa(data, descricao, valor, categoria):
    """Insere um novo gasto dentro do banco de dados."""
    conexao = conectar_banco()
    cursor = conexao.cursor()

    # No Postgres o placeholder de segurança é %s, no SQLite é ?
    placeholder = "%s" if DATABASE_URL else "?"

    cursor.execute(f"""
        INSERT INTO despesas (data, descricao, valor, categoria)
        VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder})
    """, (data, descricao, valor, categoria))

    conexao.commit()
    conexao.close()


if __name__ == "__main__":
    inicializar_banco()
