gc3 = sg.service_account("gestao.json")
link = "https://docs.google.com/spreadsheets/d/1hnV9zOAG33fFhw97RX7RERAaFDn63zKXalEJg9EJcsI/edit?usp=sharing"
sh3 = gc3.open_by_url(link)
ws3 = sh3.get_worksheet(0)
planilha3 = ws3.get_all_values()
df_teste = pd.DataFrame(planilha3[1:], columns=planilha3[0])
st.dadaframe(df_teste,use_container_width= True)
