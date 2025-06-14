import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Dados de conexão com o servidor PostgreSQL (não com um banco ainda)
conn = psycopg2.connect(
    dbname='postgres',  # banco padrão
    user='maurilio',
    password='147852',
    host='localhost'
)

# conn = psycopg2.connect(
#     dbname='postgres',
#     user='postgres',
#     password='147852',
#     host='localhost'
# )
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # necessário para CREATE DATABASE

cursor = conn.cursor()
cursor.execute("CREATE DATABASE dublin_bikes;")

cursor.close()
conn.close()

print("Banco dublin_bikes criado com sucesso.")
