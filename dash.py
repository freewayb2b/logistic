import streamlit as st
import pandas as pd
import gspread as sg
from gspread import Worksheet
import datetime as dt


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

total = df_teste["VALOR N. FISCAL"].sum()

st.write(total)

st.dataframe(df_teste,use_container_width = True, hide_index = True)


