import streamlit as st
import pandas as pd
import gspread as sg
from gspread import Worksheet
import datetime as dt

#-----------------------------------------------------------------------------------------------------
#ETL

# gc3 = sg.service_account("logistica.json")
# link = "https://docs.google.com/spreadsheets/d/1hnV9zOAG33fFhw97RX7RERAaFDn63zKXalEJg9EJcsI/edit?usp=sharing"
# sh = gc.open_by_url(link)
# ws = sh.get_worksheet(0)
# planilha = ws.get_all_values()
# df_teste = pd.DataFrame(planilha[1:], columns=planilha[0])
# st.dadaframe(df_teste,use_container_width = True, hide_index = True)

st.subheader("teste")


link = "https://docs.google.com/spreadsheets/d/1hnV9zOAG33fFhw97RX7RERAaFDn63zKXalEJg9EJcsI/edit?usp=sharing"

planilha = link
df_teste = pd.DataFrame(link)
st.dadaframe(df_teste,use_container_width = True, hide_index = True)
