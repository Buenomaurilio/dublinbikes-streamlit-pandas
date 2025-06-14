import os
import pandas as pd
from sqlalchemy import create_engine

# 1. Localizar o arquivo mais recente
pasta_bronze = '/home/maurilio/Documents/dublin_bikes/bronze/'
arquivos = [f for f in os.listdir(pasta_bronze) if f.endswith('.csv')]
arquivos.sort(reverse=True)

if not arquivos:
    print("Nenhum arquivo CSV encontrado.")
    exit()

arquivo_mais_recente = arquivos[0]
caminho_arquivo = os.path.join(pasta_bronze, arquivo_mais_recente)

# 2. Ler o CSV
df = pd.read_csv(caminho_arquivo)

df['banking'] = df['banking'].map({True: 'SIM', False: 'NAO'})
df['bonus'] = df['bonus'].map({True: 'SIM', False: 'NAO'})
print(df)
# 3. Conectar ao PostgreSQL
usuario = 'maurilio'
senha = '147852'
host = 'localhost'
porta = '5432'
banco = 'dublin_bikes'

engine = create_engine(f'postgresql://{usuario}:{senha}@{host}:{porta}/{banco}')

# 4. Inserir no banco
df.to_sql('dados_bronze', con=engine, if_exists='replace', index=False)

print(f'Dados inseridos no banco a partir de: {caminho_arquivo}')
