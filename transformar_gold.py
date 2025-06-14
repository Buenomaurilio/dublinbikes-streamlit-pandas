import pandas as pd
from sqlalchemy import create_engine

# Conecta ao banco
engine = create_engine('postgresql://maurilio:147852@localhost:5432/dublin_bikes')

# Lê dados da camada silver
df = pd.read_sql_table('dados_silver', con=engine)

# Calcula campos adicionais
df['available_stands'] = df['bike_stands'] - df['available_bikes']
df['ocupacao'] = (df['available_bikes'] / df['bike_stands']).round(2)

# Seleciona e renomeia os campos desejados
df_gold = df[[
    'number', 'name', 'available_bikes', 'bike_stands',
    'available_stands', 'ocupacao', 'last_update', 'status'
]].copy()

df_gold = df_gold.rename(columns={'last_update': 'data_hora'})

# Salva na camada gold com append (histórico)
df_gold.to_sql('dados_gold', con=engine, if_exists='append', index=False)

print("Snapshot salvo na camada gold.")

