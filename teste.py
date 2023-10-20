import streamlit as st
import pandas as pd
import datetime
from config import dia_semana

reset = False # True para resetar os dados salvos

column_qty_shown = 14

max_capacity = 6

# # # # # # # # # # # DADOS # # # # # # # # # # # 

if reset:
    df = pd.read_csv('clean.csv', index_col='Nome', dtype=str).sort_index()
else:
    df = pd.read_csv('data.csv', index_col='Nome', dtype=str).sort_index()

# os seguintes dias estarão no multiselect e no preview:

dias = []
for i in range(column_qty_shown):
    today = datetime.date.today() + datetime.timedelta(days=i)
    date = today.strftime('%d/%m')
    weekday = dia_semana(today.weekday())
    date = f'{weekday}, {date}'
    dias += [date]

for i in dias:
    if i not in df.columns:
        df[i] = None

# # # # # # # # # # # STREAMLIT # # # # # # # # # # # 

st.set_page_config(layout="wide")


# left 
with st.sidebar:
    nome = st.selectbox(
        'Selecione seu nome.', (df.index),
        placeholder="Nome",
        index=None)

    dias_selecionados = st.multiselect(
        'Selecione os dias que você irá ao CCS.', (dias),
        placeholder="Dia(s) no presencial")

    botao_submeter = st.button("Submeter presença", type="primary")

    botao_limpar = st.button("Limpar tudo do usuário selecionado")

    if botao_submeter and nome is not None and dias_selecionados is not None:
        for i in dias_selecionados:
            if df[i].count() >= max_capacity:
                st.write(f'Erro em {i}: **capacidade atingida**!')

            if df[i].count() < max_capacity:      
                df.loc[nome, i] = '✅'
                st.write(f'Submetido: {i}')

            if df[i].count() == max_capacity:
                df[i] = df[i].fillna('❌')

            df.to_csv(f'data.csv')
    
    if botao_limpar and nome is not None and dias_selecionados is not None:
        for i in dias:
            df.loc[nome, i] = None
            if df[i].count() != max_capacity:
                df[i] = df[i].replace('❌', None)
            df.to_csv(f'data.csv')
        st.write('Tudo limpo!')

# right
st.title('White Team: controle de baias')
st.dataframe(data=df[dias], height = 568)
st.write('*A capacidade atual é de até seis (6) pessoas em cada dia.')