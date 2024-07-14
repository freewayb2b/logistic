import folium.map
import streamlit as st
import pandas as pd
import datetime as dt
import plotly.express as px
from streamlit_folium import st_folium

#-----------------------------------------------------------------------------------------------------
#page config

st.set_page_config(layout = "wide",page_title="Logística FW",page_icon="🚚")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html = True)

st.title("Visão Geral - Logística Freeway", anchor= False)
st.divider()

col1, col2, col3, col4, col5 = st.columns([2,2,2,1,1])
col6, col7= st.columns(2)
col8, = st.columns(1)


#-----------------------------------------------------------------------------------------------------
#ETL

link = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ_InxkV5GPZKYxQp1qO9d1knpB4_xzbh-TL0YYDor-wY1ldpmOisnRDZ6imGvt6d14rz8IRS7ivN3K/pub?output=csv"

df = pd.read_csv(link)

df["Data"] = pd.to_datetime(df["DATA N.F."])
df["Mês"] = pd.to_datetime(df["DATA N.F."]).dt.day
df["dia"] = pd.to_datetime(df["DATA N.F."]).dt.month
df["Ano"] = df["Data"].dt.year
df['data_string'] = df['Ano'].astype(str) + '-' + df['Mês'].astype(str).str.zfill(2) + '-' + df['dia'].astype(str).str.zfill(2)


df = df.drop(columns=["TNT FRANCA","%","%.1","%.2","%.3","%.4","%.5","%.6","TNT JACOBINA","MENOR VR. FRETE","TRANSP. MENOR FRETE",'data_string',"Data",
                "%.7","F.L. LOG.","TROCA TRANS.","VITLOG","RODO-NAVES","VR. FRETE CALCULADO N.F.","VR. DIFER."])

df['FRETE PAGO'] = df['VR. FRETE COBRADO'].str.replace('.', '').str.replace(',', '.').astype(float)
df['VALOR N.FISCAL'] = df['VALOR N.FISCAL'].str.replace('.', '').str.replace(',', '.').astype(float)


#-----------------------------------------------------------------------------------------------------
#mapear meses

mapear_meses = {
        1:'Jan',
        2:'Fev',
        3:'Mar',
        4:'Abr',
        5:'Mai',
        6:'Jun',
        7:'Jul',
        8:'Ago',
        9:'Set',
        10:'Out',
        11:'Nov',
        12:'Dez'
}
df = df.sort_values('Mês', ascending= True)

df["Mês"] = df["Mês"].map(mapear_meses)


#-----------------------------------------------------------------------------------------------------
#filters

with col4:
    filter_year = st.selectbox('Ano', df["Ano"].unique())
with col5:
    filter_month = st.selectbox('Mês',df["Mês"].unique())

df_filtrado = df.query('Ano == @filter_year and Mês == @filter_month')
df_filtrado = df_filtrado.drop(columns=["Ano","VR. FRETE COBRADO","VR. FRETE COTAÇAO"])


qtd_nfs = df_filtrado.shape[0]
total = df_filtrado["VALOR N.FISCAL"].sum()
valor_frete = df_filtrado["FRETE PAGO"].sum()

with col1:
    st.metric("QTD NFs",qtd_nfs)
    
with col2:
    st.metric("Total Faturado",f'R$ {total:,.0f}')
    
with col3:
    st.metric("Total Fretes",f'R$ {valor_frete:,.0f}')

#-----------------------------------------------------------------------------------------------------
#charts 
df_columns = df_filtrado.groupby('dia')['FRETE PAGO'].sum().reset_index()
area_chart = px.area(df_columns,x="dia", y="FRETE PAGO",title="Acompanhamento Diário")

with col6:
    st.plotly_chart(area_chart,use_container_width= True)

df_bar = df_filtrado.groupby('TRANSPORTADORA')['FRETE PAGO'].sum().reset_index()
df_bar = df_bar.sort_values("FRETE PAGO",ascending = True)
bar_chart = px.bar(df_bar,x="FRETE PAGO", y="TRANSPORTADORA",title="Frete Por Transportadora",orientation= "h")
with col7:
    st.plotly_chart(bar_chart,use_container_width= True)

df_faturamento = df_filtrado.groupby('dia')['VALOR N.FISCAL'].sum().reset_index()
area_chart_faturamento = px.area(df_faturamento,x="dia", y="VALOR N.FISCAL",title="Faturamento Diário")

with col8:
    st.plotly_chart(area_chart_faturamento,use_container_width= True)

  
st.dataframe(df_filtrado,use_container_width = True, hide_index = True)
#-----------------------------------------------------------------------------------------------------

