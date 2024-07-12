import streamlit as st
import pandas as pd
import gspread as sg
from gspread import Worksheet
import datetime as dt
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px


st.set_page_config(layout = "wide")
#-----------------------------------------------------------------------------------------------------
#ETL

# gc = sg.service_account("logistica.json")
# link = "https://docs.google.com/spreadsheets/d/1hnV9zOAG33fFhw97RX7RERAaFDn63zKXalEJg9EJcsI/edit?usp=sharing"
# sh = gc.open_by_url(link)
# ws = sh.get_worksheet(0)
# planilha = ws.get_all_values()
# df_teste = pd.DataFrame(planilha[1:], columns=planilha[0])
# st.dataframe(df_teste,use_container_width = True, hide_index = True)

st.subheader("teste")


link = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ_InxkV5GPZKYxQp1qO9d1knpB4_xzbh-TL0YYDor-wY1ldpmOisnRDZ6imGvt6d14rz8IRS7ivN3K/pub?output=csv"

df_teste = pd.read_csv(link)
df_teste['Data'] = pd.to_datetime(df_teste["DATA N.F."])
df_teste["Mês"] = df_teste["Data"].dt.month


df_teste = df_teste.drop(columns=["TNT FRANCA","%","%.1","%.2","%.3","%.4","%.5","%.6","%.7","F.L. LOG.","TROCA TRANS.","VITLOG","RODO-NAVES","VR. FRETE CALCULADO N.F.","VR. DIFER."])

df_teste['VR. FRETE COBRADO'] = df_teste['VR. FRETE COBRADO'].str.replace('.', '').str.replace(',', '.').astype(float)



filto_trans = st.selectbox("",df_teste["TRANSPORTADORA"].unique())

df_filtrado = df_teste.query('TRANSPORTADORA == @filto_trans')

total = df_filtrado["VR. FRETE COBRADO"].sum()
st.metric("Pago",f'R$ {total:,.2f}')

st.dataframe(df_filtrado,use_container_width = True, hide_index = True)




# Criar um DataFrame de exemplo com nomes de estados e valores
data = {
    'state': ['São Paulo', 'Rio de Janeiro', 'Minas Gerais', 'Bahia', 'Paraná'],
    'value': [100, 150, 200, 250, 300]
}

df = pd.DataFrame(data)

# Carregar o shapefile de estados do Brasil
brasil = gpd.read_file('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson')

# brasil = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Mesclar o GeoDataFrame do Brasil com o DataFrame dos valores
brasil = brasil.merge(df, how='left', left_on='name', right_on='state')

# Configurações de layout do Streamlit
st.title('Mapa de Valores por Estado no Brasil')

# Plotar o mapa usando o Streamlit
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
brasil.plot(column='value', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
plt.title('Valores por Estado no Brasil')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Mostrar o mapa no Streamlit
st.plotly_chart(fig)


