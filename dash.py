import streamlit as st
import pandas as pd
import datetime as dt
import plotly.express as px

#-----------------------------------------------------------------------------------------------------
#page config

st.set_page_config(layout = "wide",page_title="Logística FW",page_icon="🚚")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html = True)

st.image("header.png")
st.divider()


coltitle, = st.columns(1)
col1, col2, col3, col4, col5, col6 = st.columns([1.8,1.8,1.8,1.5,1,1])
col7, col8 = st.columns(2)
col10, col11 = st.columns(2)
col9, = st.columns(1)
col12, = st.columns(1)

#-----------------------------------------------------------------------------------------------------
#ETL

link = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ_InxkV5GPZKYxQp1qO9d1knpB4_xzbh-TL0YYDor-wY1ldpmOisnRDZ6imGvt6d14rz8IRS7ivN3K/pub?output=csv"


@st.cache_data
def load_data(link):
    dados = pd.read_csv(link)
    return dados

df = load_data(link)


df["Data"] = pd.to_datetime(df["DATA N.F."])

df["Mês"] = pd.to_datetime(df["DATA N.F."]).dt.month
df["dia"] = pd.to_datetime(df["DATA N.F."]).dt.day
df["Ano"] = df["Data"].dt.year
df['data_string'] = df['Ano'].astype(str) + '-' + df['Mês'].astype(str).str.zfill(2) + '-' + df['dia'].astype(str).str.zfill(2)
df["DATA N.F."] = df['data_string']
df["DATA N.F."] = pd.to_datetime(df["DATA N.F."])

# df = df.drop(columns=["TNT FRANCA","%","%.1","%.2","%.3","%.4","%.5","%.6","TNT JACOBINA","MENOR VR. FRETE","TRANSP. MENOR FRETE",'data_string',"Data",
#                 "%.7","F.L. LOG.","TROCA TRANS.","VITLOG","RODO-NAVES","VR. FRETE CALCULADO N.F.","VR. DIFER."])

df['FRETE PAGO'] = df['VR. FRETE COBRADO'].str.replace('.', '').str.replace(',', '.').astype(float)
df['VALOR N.FISCAL'] = df['VALOR N.FISCAL'].str.replace('.', '').str.replace(',', '.').astype(float)

#-----------------------------------------------------------------------------------------
#renomear transportadoras
df['TRANSPORTADORA'] = df['TRANSPORTADORA'].str.replace('RODONAVES TRANSP E ENCOMENDAS LTDA', 'RODONAVES')
df['TRANSPORTADORA'] = df['TRANSPORTADORA'].str.replace('RODONAVES TRANSP ENC LTDA', 'RODONAVES')
df['TRANSPORTADORA'] = df['TRANSPORTADORA'].str.replace('TNT MERCURIO CARGAS E ENCOMENDAS EXPRESS', 'TNT')
df['TRANSPORTADORA'] = df['TRANSPORTADORA'].str.replace('TRANSPORTES TRANSLOVATO LTDA', 'TRANSLOVATO')
df['TRANSPORTADORA'] = df['TRANSPORTADORA'].str.replace('VIACAO GARCIA LTDA', 'VIACAO GARCIA')
df['TRANSPORTADORA'] = df['TRANSPORTADORA'].str.replace('MOVVI LOGÍSTICA LTDA', 'MOVVI')
df['TRANSPORTADORA'] = df['TRANSPORTADORA'].str.replace('UNIÃO TRANSP DE ENCOMENDAS E COM. E VEIC', 'UNIÃO')
df['TRANSPORTADORA'] = df['TRANSPORTADORA'].str.replace('TRANSLAGUNA ARMAZENAGEM E TRANSP EIRELI', 'TRANSLAGUNA')
df['TRANSPORTADORA'] = df['TRANSPORTADORA'].str.replace('BRASPRESS TRANSPORTES URGENTES LTDA', 'BRASPRESS')
df['TRANSPORTADORA'] = df['TRANSPORTADORA'].str.replace('VITORIA PROVEDORA LOGISTICA LTDA', 'VITLOG')
df['TRANSPORTADORA'] = df['TRANSPORTADORA'].str.replace('PATRUS TRANSPORTES LTDA', 'PATRUS')
df['TRANSPORTADORA'] = df['TRANSPORTADORA'].str.replace('PATRUS TRANSPORTES URGENTES LTDA', 'PATRUS')
df['TRANSPORTADORA'] = df['TRANSPORTADORA'].str.replace('FL BRASIL HOLDING, LOG E TRANSPORTE LTDA', 'SOLISTICA')
df['TRANSPORTADORA'] = df['TRANSPORTADORA'].str.replace('FEDEX BRASIL LOGISTICA E TRANSPORTE S.A', 'FEDEX')
df['TRANSPORTADORA'] = df['TRANSPORTADORA'].str.replace('RODONAVES TRANSPORTES E ENCOM.  LTDA', 'RODONAVES')
df['TRANSPORTADORA'] = df['TRANSPORTADORA'].str.replace('TNT MERCURIO CARGAS E ENCOMENDAS', 'TNT')
df['TRANSPORTADORA'] = df['TRANSPORTADORA'].str.replace('RACE OPERADOR LOGISTICO EIRELI', 'RACE')
df['TRANSPORTADORA'] = df['TRANSPORTADORA'].str.replace('MENGUE EXPRESS TRANSPORTES LTDA', 'MENGUE EXPRESS')


#-----------------------------------------------------------------------------------------------------


df["UNIDADE"] = df['N. F.'].astype(str).str.slice(0, 1)
df['UNIDADE'] = df['UNIDADE'].str.replace('1', 'Jacobina').str.replace('3', 'Franca')


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
#mes atual

today = dt.date.today()

mes = today.month

if mes == 1:
    mes_atual = "Jan"
elif mes == 2:
    mes_atual = "Fev"
elif mes == 3:
    mes_atual = "Mar"
elif mes == 4:
    mes_atual = "Abr"
elif mes == 5:
    mes_atual = "Mai"
elif mes == 6:
    mes_atual = "Jun"
elif mes ==7:    
    mes_atual = "Jul"
elif mes == 8:    
    mes_atual = "Ago"
elif mes == 9:    
   mes_atual =  "Set"
elif mes == 10:    
   mes_atual =  "Out"
elif mes == 11:    
    mes_atual = "Nov"
else:
    "Dez"

meses = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']

#-----------------------------------------------------------------------------------------------------
#filters

with coltitle:
    filtro_fabrica = st.multiselect("Unidade",["Franca","Jacobina"],default = ["Franca","Jacobina"])
with col5:
    filtro_inicio = st.date_input("De",pd.to_datetime("2023-01-01").date(),format= "DD/MM/YYYY")
with col6:
    filtro_fim = st.date_input("Até","today",format= "DD/MM/YYYY")



df_filtrado = df.groupby(['UNIDADE','N. F.','DATA N.F.','CIDADE','UF','TRANSPORTADORA','Ano','Mês',"dia"])['VALOR N.FISCAL'].sum().reset_index()

df_filtrado = df_filtrado.query('@filtro_inicio <= `DATA N.F.` <= @filtro_fim and UNIDADE == @filtro_fabrica')


#---------------------------------------------------------------------------------------------

df_proc = df.drop_duplicates(subset='N. F.', keep='first')

df_filtrado = pd.merge(df_filtrado, df_proc[['N. F.', 'FRETE PAGO']], on='N. F.', how='left')

df_filtrado['PERC. %'] = df_filtrado.apply(lambda row: (row['FRETE PAGO'] / row['VALOR N.FISCAL']) * 100, axis=1)
df_filtrado['PERC. %'] = df_filtrado['PERC. %'].apply(lambda x: f"{x :.1f}%")

#-----------------------------------------------------------------------------------------------------

qtd_nfs = df_filtrado.shape[0]
total = df_filtrado["VALOR N.FISCAL"].sum()
valor_frete = df_filtrado["FRETE PAGO"].sum()
percentual_frete = (valor_frete / total) * 100
percentual_frete = f"{percentual_frete:.2f}%"


#-----------------------------------------------------------------------------------------------------

with col1:
    st.metric("Total Faturado",f'💰 R$ {total:,.0f}')
    
with col2:
    st.metric("QTD NFs",f'📃 {qtd_nfs:,.0f}')
    
    
with col3:
    st.metric("Frete Pago",f'💵 R$ {valor_frete:,.0f}')

with col4:
    st.metric("Percentual Frete",f'🚚 {percentual_frete}')

#-----------------------------------------------------------------------------------------------------
#charts colors
cor_barras = "#000000"

#-----------------------------------------------------------------------------------------------------
#table

df_table = df_filtrado.groupby('TRANSPORTADORA').agg({'VALOR N.FISCAL': 'sum','FRETE PAGO': 'sum'}).reset_index()
df_table = df_table.sort_values("FRETE PAGO",ascending = False)
df_table['PERC. %'] = df_table.apply(lambda row: (row['FRETE PAGO'] / row['VALOR N.FISCAL']) * 100, axis=1)
df_table['PERC. %'] = df_table['PERC. %'].apply(lambda x: f"{x :.1f}%")
df_table['FRETE PAGO'] = df_table['FRETE PAGO'].apply(lambda x: f'R$ {x:,.2f}')
df_table['VALOR N.FISCAL'] = df_table['VALOR N.FISCAL'].apply(lambda x: f'R$ {x:,.2f}')


with col8:
    st.subheader("Por Transportadora", anchor = False)
    st.dataframe(df_table,use_container_width= True, hide_index = True)



df_pie = df_filtrado.groupby('UNIDADE')['FRETE PAGO'].sum().reset_index()    

pie_chart = px.pie(df_pie,values = "FRETE PAGO", names ="UNIDADE",
category_orders = {'UNIDADE':["Franca","Jacobina"]},color_discrete_sequence=["#9AA5A7","#3E4A4A"])
pie_chart.update_traces(showlegend=True,textfont=dict(size=17,color='#ffffff'),textposition='outside')


with col7:
    st.subheader("Frete Por Unidade",anchor=False)
    st.plotly_chart(pie_chart,use_container_width= True)


#-----------------------------------------------------------------------------------------------------

df_faturamento = df_filtrado.groupby('dia')['VALOR N.FISCAL'].sum().reset_index()


column_chart_faturamento = px.area(df_faturamento,x="dia", y="VALOR N.FISCAL",color_discrete_sequence=[cor_barras])
column_chart_faturamento.update_xaxes(dtick=1)
column_chart_faturamento.layout.xaxis.fixedrange = True
column_chart_faturamento.layout.yaxis.fixedrange = True
column_chart_faturamento.update_xaxes(showgrid= False,visible = True ,title="")

with col9:
    st.subheader("Faturamento Diário", anchor = False)
    st.plotly_chart(column_chart_faturamento,use_container_width= True)
#-----------------------------------------------------------------------------------------------------

df_filtrado = df_filtrado.drop(columns=["Mês","dia","Ano"])
df_filtrado["DATA N.F."] = df_filtrado["DATA N.F."].dt.strftime('%d/%m/%Y')
#-----------------------------------------------------------------------------------------------------

df_uf = df_filtrado.groupby('UF')['VALOR N.FISCAL'].sum().reset_index()
df_uf['FATURAMENTO'] = df_uf['VALOR N.FISCAL']
df_uf = df_uf.drop(columns="VALOR N.FISCAL")
df_uf = df_uf.sort_values('FATURAMENTO',ascending=False)
df_uf['FATURAMENTO'] = df_uf['FATURAMENTO'].apply(lambda x: f'R$ {x:,.2f}')

#-----------------------------------------------------------------------------------------------------

df_uf_frete = df_filtrado.groupby('UF').agg({'VALOR N.FISCAL': 'sum','FRETE PAGO': 'sum'}).reset_index()
df_uf_frete['PERC. %'] = df_uf_frete.apply(lambda row: (row['FRETE PAGO'] / row['VALOR N.FISCAL']) * 100, axis=1)
df_uf_frete['PERC. %'] = df_uf_frete['PERC. %'].apply(lambda x: f"{x :.1f}%")
df_uf_frete = df_uf_frete.sort_values('VALOR N.FISCAL',ascending=False)
df_uf_frete['FRETE PAGO'] = df_uf_frete['FRETE PAGO'].apply(lambda x: f'R$ {x:,.2f}')
df_uf_frete['VALOR N.FISCAL'] = df_uf_frete['VALOR N.FISCAL'].apply(lambda x: f'R$ {x:,.2f}')



#-----------------------------------------------------------------------------------------------------
df_filtrado['FRETE PAGO'] = df_filtrado['FRETE PAGO'].apply(lambda x: f'R$ {x:,.2f}')
df_filtrado['VALOR N.FISCAL'] = df_filtrado['VALOR N.FISCAL'].apply(lambda x: f'R$ {x:,.2f}')


with col12:
    st.subheader("Detalhamento Geral", anchor = False)
    st.dataframe(df_filtrado,use_container_width = True, hide_index = True)

with col10:
    st.subheader("Faturamento Por Estado", anchor = False)
    st.dataframe(df_uf,use_container_width = True, hide_index = True)


with col11:
    st.subheader("Faturamento X Percentual Frete", anchor = False)
    st.dataframe(df_uf_frete,use_container_width = True, hide_index = True)
    
#-----------------------------------------------------------------------------------------------------
#estilizacao

borda = """
            <style>
            [data-testid="stColumn"]
            {
            background-color: #2F3035;
            border-radius: 15px;
            padding: 10px;
            text-align: center;
            color: #ffffff;
            opacity: 100%;
            }
            </style>
            """

st.markdown(borda, unsafe_allow_html=True)  



botao = """
            <style>
            [data-testid="StyledFullScreenButton"]
            {
            visibility: hidden;
            }
            </style>
            """

st.markdown(botao, unsafe_allow_html=True)  
