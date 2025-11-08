import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from utils.totalizadores import (total_acidentes,total_feridos,total_mortos,total_veiculos)
from utils.filtros import filtros_aplicados, filtro_mes_nome
from utils import sobre, dataframe, paines
# Entrada de dados
@st.cache_data
def carregar_arquivo_parquet(CAMINHO_ARQUIVO):
    try:
        return pd.read_parquet(CAMINHO_ARQUIVO, engine='pyarrow')
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {e}")
        return pd.DataFrame()  # retorna dataframe vazio para evitar crash


# Titulo da página
def titulo_pagina(primeira_data, ultima_data, hoje):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            f"""
            <h1>PRF - Acidentes Rodovias Federais</h1>
            <p>Fonte: Dados abertos da PRF</p>
            <p>Período: {primeira_data} a {ultima_data}</p>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div style="margin-top: 40px;">
                <a href="https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf" 
                   target="_blank" class="botao-link">
                    🔗 Acessar fonte dos dados
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write(f"📅 Data: {hoje.strftime('%d/%m/%Y')}")

# Inicialização dos filtros globais
def iniciar_filtros_globais(filtros_iniciais):
    for filtro in filtros_iniciais:
        chave = f'main_filtro_{filtro}'
        if chave not in st.session_state:
            st.session_state[chave] = []


# Funcao de navegacao geral do app
def criacao_navegacao_e_filtros(df):
    df_filtrado = df.copy()

    with st.sidebar:
        selected = option_menu(
            menu_title="Navegue nas páginas",
            options=["Sobre", "Painéis", "Dataframe"],
            icons=["info-circle", "bar-chart", "table"],
            menu_icon="cast",
            default_index=0
        )
        st.markdown("<h1>Filtros</h1>", unsafe_allow_html=True)
        
        df_filtrado = filtros_aplicados(df_filtrado, 'Ano')
        df_filtrado = filtro_mes_nome(df_filtrado)
        df_filtrado = filtros_aplicados(df_filtrado, 'Região')
        df_filtrado = filtros_aplicados(df_filtrado, 'Uf')
        df_filtrado = filtros_aplicados(df_filtrado, 'Municipio')
        

    c1, c2, c3, c4 = st.columns(4,gap="small")

    with c1.container(border=True):
        st.metric("🚨 Acidentes", total_acidentes(df_filtrado))

    with c2.container(border=True):   
        st.metric("💀 Mortos", total_mortos(df_filtrado))

    with c3.container(border=True):
        st.metric("🩹 Feridos", total_feridos(df_filtrado))
            
    with c4.container(border=True):
        st.metric("🚗 Veiculos", total_veiculos(df_filtrado))
    
    # Navegação do sistema
    if selected == "Sobre":
        sobre.mainSobre()
    elif selected == "Painéis":
        paines.mainGraficos(df_filtrado)
    else:
        dataframe.mainDataframe(df_filtrado)
    