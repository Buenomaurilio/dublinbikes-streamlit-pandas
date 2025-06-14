import ast
import json
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Conexão com o banco PostgreSQL
engine = create_engine('postgresql://maurilio:147852@localhost:5432/dublin_bikes')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Definindo a tabela Silver
class DadosSilver(Base):
    __tablename__ = 'dados_silver'

    number = Column(Integer, primary_key=True)
    contract_name = Column(String)
    name = Column(String)
    address = Column(String)
    banking = Column(String)
    bonus = Column(String)
    status = Column(String)
    bike_stands = Column(Integer)
    available_bike_stands = Column(Integer)
    available_bikes = Column(Integer)
    last_update = Column(DateTime)
    data_coleta = Column(DateTime)
    latitude = Column(Float)
    longitude = Column(Float)

# Criar tabela se não existir
Base.metadata.create_all(engine)

# Ler dados da camada bronze
df = pd.read_sql_table('dados_bronze', con=engine)

print(df)
print(50*'=')
# Aplicar os tratamentos



df['position'] = df['position'].apply(ast.literal_eval)

df['latitude'] = df['position'].apply(lambda x: x['lat'])
df['longitude'] = df['position'].apply(lambda x: x['lng'])

df = df.drop(columns=['position'])

df['number'] = df['number'].astype(int)
df['contract_name'] = df['contract_name'].astype(str)
df['last_update'] = pd.to_datetime(df['last_update'], unit='ms')
# print(df)
# Inserir na camada silver
df.to_sql('dados_silver', con=engine, if_exists='replace', index=False)

print("Dados salvos na camada silver.")
