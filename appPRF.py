import streamlit as st
import pandas as pd
import sys
import os
from datetime import date
from streamlit_option_menu import option_menu
# Agora importa os módulos da pasta utils
from utils import sobre, dataframe, paines, marcadores
from utils.totalizadores import total_acidentes,total_feridos,total_mortos,total_veiculos #, total_ilesos
from utils.marcadores import divisor
from utils.filtros import filtros_aplicados, filtro_mes_nome
# ----------------------------
# Configuração da página. Fica sempre no início do projeto
# ----------------------------
st.set_page_config(
    layout="wide",
    page_title="PRF2023a2025"
)

# ----------------------------
# Ajusta path para encontrar utils
# ----------------------------
sys.path.append(os.path.join(os.path.dirname(__file__), "utils"))

# ----------------------------
# Data atual
# ----------------------------
hoje = date.today()

# ----------------------------
# Inicialização dos filtros globais
# ----------------------------
filtros_iniciais = ['Ano', 'Mês', 'Região', 'Estado', 'Municipio', 'Grupo Via', 'Classificacao Acidente']
for filtro in filtros_iniciais:
    chave = f'main_filtro_{filtro}'
    if chave not in st.session_state:
        st.session_state[chave] = []

# ----------------------------
# Caminho do arquivo
# ----------------------------
CAMINHO_ARQUIVO = "Dados/PRF2023a2025.parquet"

# ----------------------------
# Função para carregar arquivo Parquet
# ----------------------------
@st.cache_data
def carregar_arquivo_parquet():
    try:
        return pd.read_parquet(CAMINHO_ARQUIVO, engine='pyarrow')
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {e}")
        return pd.DataFrame()  # retorna dataframe vazio para evitar crash

df = carregar_arquivo_parquet()

# ----------------------------
# Cópia do DataFrame original
# ----------------------------
df_filtrado = df.copy()

# Última e primeira data
ultima_data = df['Data Inversa'].max().strftime("%d/%m/%Y") if not df.empty else None
primeira_data = df['Data Inversa'].min().strftime("%d/%m/%Y") if not df.empty else None



# ----------------------------
# Função do título da página
# ----------------------------
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
    divisor()
        #st.write("Desenvolvido por Ben-Hur Queiroz Beltrão")
     


# ----------------------------
# Função principal de navegação e filtros
# ----------------------------
def criacao_navegacao_e_filtros():
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
        df_filtrado = filtros_aplicados(df_filtrado, 'Estado')
        df_filtrado = filtros_aplicados(df_filtrado, 'Municipio')
        

    c1, c2, c3, c4= st.columns(4,gap="small")

    with c1.container(border=True):
        st.metric("Sinistros", total_acidentes(df_filtrado))

    with c2.container(border=True):   
        st.metric("Mortos", total_mortos(df_filtrado))

    with c3.container(border=True):
        st.metric("Feridos", total_feridos(df_filtrado))
            
    with c4.container(border=True):
        st.metric("Veiculos", total_veiculos(df_filtrado))

    #with c4.container(border=True):
        #st.metric("Ilesos", total_ilesos(df_filtrado))  

    # DataFrame para gráfico de linha
    #df_filtrado_linha = df.copy()
    #for col in ['Tipo_Imovel','Tipo_Ocupacao','Região','Bairro']:
        #key = f'main_filtro_{col}'
        #if key in st.session_state and st.session_state[key]:
           # df_filtrado_linha = df_filtrado_linha[df_filtrado_linha[col].isin(st.session_state[key])]

    #totalLinhas = df_filtrado.shape[0]

    # Conteúdo principal
    if selected == "Sobre":
        sobre.mainSobre()

    elif selected == "Painéis":
        #df_filtrado_linha['Ano'] = df_filtrado_linha['Ano'].astype(str)
        paines.mainGraficos(df_filtrado)
    else:
        dataframe.mainDataframe(df_filtrado)


# ----------------------------
# Função main
# ----------------------------
def main():
    titulo_pagina(primeira_data, ultima_data, hoje)
    criacao_navegacao_e_filtros()

# ----------------------------
# Executa o app
# ----------------------------
if __name__ == '__main__':
    main()
