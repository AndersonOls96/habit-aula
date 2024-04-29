import sqlite3

habits_to_insert = [
    ('Estudar inglês', 0),
    ('Praticar violão', 0),
    ('Estudar Flet', 0),
]

conn = sqlite3.connect('habits.db')
cursor = conn.cursor()

# Instrução SQL para inserir um hábito
insert_query = 'INSERT INTO habits (title, done) VALUES (?, ?)'

# Inserir os hábitos na tabela
cursor.executemany(insert_query, habits_to_insert)

# Salvar (commit) as mudanças
conn.commit()

# Fechar a conexão com o banco de dados
conn.close()