from sqlalchemy import create_engine, text

# Criar uma engine para se conectar ao banco de dados SQLite
db_engine = create_engine('sqlite:///exemplo.db')

# Criar a tabela 'user' no banco de dados
create_table_query = """
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
)
"""
with db_engine.connect() as connection:
    connection.execute(text(create_table_query))