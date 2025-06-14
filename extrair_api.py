import os
import pandas as pd
import requests
from datetime import datetime

def d_bikes():
    url = 'https://api.jcdecaux.com/vls/v1/stations'
    api_key = '5c07ed433d8e7357f3fc3abb861d9eb6c79c8163'

    params = {
        'contract': 'Dublin',
        'apiKey': api_key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        # print("Erro ao acessar a API")
        return []

data = d_bikes()
df_pandas = pd.DataFrame(data)
print(df_pandas)

# Criar diretório de saída
output_dir = '/home/maurilio/Documents/dublin_bikes/bronze'
os.makedirs(output_dir, exist_ok=True)

# Nome do arquivo com timestamp (opcional)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
file_path = os.path.join(output_dir, f'dublin_bikes_raw_{timestamp}.csv')

# Salvar como CSV
df_pandas.to_csv(file_path, index=False)

print(df_pandas)
print(f'Dados salvos em: {file_path}')
