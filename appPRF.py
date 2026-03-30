# Importação das bibliotecas
import streamlit as st
import pandas as pd
import sys
import os

# Importação dos módulos
from datetime import date
from utils.totalizadores import ( calculo_data_inicial_df, calculo_data_final_df)
from utils.funcoes import titulo_pagina, carregar_arquivo_parquet, iniciar_filtros_globais, criacao_navegacao_e_filtros


# Configuração da página. Fica sempre no início do projeto
st.set_page_config(
    layout="wide",
    page_title="Acidentes PRF 2021 a 2026"
)

# Ajusta path para encontrar utils
sys.path.append(os.path.join(os.path.dirname(__file__), "utils"))


# Data atual
hoje = date.today()

# Caminho do arquivo
CAMINHO_ARQUIVO = "Dados/PRF2023a2026.parquet"

# Entrada de dados
df = carregar_arquivo_parquet(CAMINHO_ARQUIVO)


# Cópia do DataFrame original
df_filtrado = df.copy()

# Cálculo do período do df
primeira_data = calculo_data_inicial_df(df, 'Data')
ultima_data = calculo_data_final_df(df, 'Data')


# Função
def main():
    titulo_pagina(primeira_data, ultima_data, hoje)
    filtros_iniciais = ['Ano', 'Mês', 'Região', 'Estado', 'Municipio', 'Grupo Via', 'Classificacao Acidente']
    iniciar_filtros_globais(filtros_iniciais)
    criacao_navegacao_e_filtros(df)


# Executa o app

if __name__ == '__main__':
    main()
