import sqlite3

def criar_conexao():
    conn = sqlite3.connect('usuarios.db')
    return conn

def criar_banco_usuarios():
    conn = criar_conexao()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    criar_banco_usuarios()
