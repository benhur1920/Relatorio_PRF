import pandas as pd
import streamlit as st



# ----------------------------
# Funções de filtro
# ----------------------------

def filtros_aplicados(df, nome_do_filtro):
    chave = f'main_filtro_{nome_do_filtro}'
    
    # Inicializa o session_state caso ainda não exista
    if chave not in st.session_state:
        st.session_state[chave] = []

    # Widget Multiselect
    filtro_opcao = st.multiselect(
        f'Selecione {nome_do_filtro}',
        options=sorted(df[nome_do_filtro].dropna().unique()),
        default=st.session_state[chave],
        key=chave
    )
    
    # Atualiza o session_state automaticamente (Streamlit faz isso ao usar key)
    # Apenas filtra os dados com base no valor atual
    return df[df[nome_do_filtro].isin(st.session_state[chave])] if st.session_state[chave] else df
def filtro_mes_nome(df):
    meses_ordenados = {
        'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4,
        'Maio': 5, 'Junho': 6, 'Julho': 7, 'Agosto': 8,
        'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12
    }
    
    chave = 'main_filtro_mes'
    
    if chave not in st.session_state:
        st.session_state[chave] = []

    opcoes_disponiveis = sorted(
        df['Mês'].dropna().unique(),
        key=lambda x: meses_ordenados.get(x, 99)
    )

    filtro_opcao = st.multiselect(
        'Selecione o Mês',
        options=opcoes_disponiveis,
        default=st.session_state[chave],
        key=chave
    )
    
    return df[df['Mês'].isin(st.session_state[chave])] if st.session_state[chave] else df
