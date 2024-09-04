import pandas as pd
import requests
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import folium

st.title('''DublinBikes app''')

@st.cache_data
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


data = d_bikes()

df_pandas = pd.DataFrame(data)

# print(df_pandas)

df_pandas['latitude'] = df_pandas['position'].apply(lambda x: x['lat'])
df_pandas['longitude'] = df_pandas['position'].apply(lambda x: x['lng'])

df_pandas = df_pandas.drop(columns=['position'])
df_pandas['banking'] = df_pandas['banking'].map({True: 'SIM', False: 'NAO'})
df_pandas['bonus'] = df_pandas['bonus'].map({True: 'SIM', False: 'NAO'})

df_pandas['number'] = df_pandas['number'].astype(int)
df_pandas['contract_name'] = df_pandas['contract_name'].astype(str)

df_pandas['last_update'] = pd.to_datetime(df_pandas['last_update'], unit='ms')

print(df_pandas)

if st.checkbox('Show raw data'):
    st.write(df_pandas)

st.subheader('Number of Bikes Available per Station')
fig, ax = plt.subplots(figsize=(20, 10))
df_pandas.plot(kind='bar', x='name', y='available_bikes', ax=ax, color='skyblue')
plt.xticks(rotation=90, ha='right', fontsize=7)
plt.xlabel('Station')
plt.ylabel('Available Bikes')
plt.title('Available Bikes by Station')

plt.yticks(np.arange(0, 45, 1))

plt.subplots_adjust(bottom=0.01)

st.pyplot(fig)

m = folium.Map(location=[53.349805, -6.26031], zoom_start=14)


marker_cluster = MarkerCluster().add_to(m)

for _, row in df_pandas.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"{row['name']}: {row['available_bikes']} available bikes",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(marker_cluster)


st.subheader('Interactive Map with Bicycle Stations.')
st.markdown("The map below shows the location of the bike stations and the quantity available at each one.")
st_folium(m, width=2000)
