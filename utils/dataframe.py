import streamlit as st
from utils.marcadores import divisor
#from utils.totalizadores import calular_a_quantidade_de_colunas
import pandas as pd

def dataframe(df_filtrado):
    
    if df_filtrado.shape[0] > 1:
    
        st.markdown(
            f"""
            <div style="text-align: center; margin-top: 60px">
                <h3>Download dos dados</h3>
                            
            </div>
            """, unsafe_allow_html=True
        )
        
        #st.dataframe(df_filtrado)
        # Seleção de colunas
        with st.expander('Clique para selecionar as colunas  que deseja para download do seu arquivo .csv na seta'):
            colunas = st.multiselect(
                'Selecione as Colunas',
                options=list(df_filtrado.columns),
                default=list(df_filtrado.columns),
                
            )
        
        filtro_dados=df_filtrado.copy()
        # Aplica seleção de colunas
        filtro_dados = filtro_dados[colunas]

        # CSS custom para o data editor
        st.markdown("""
            <style>
            .stDataFrame, .stDataEditor {
                background-color: #444444 !important;
            }
            </style>
        """, unsafe_allow_html=True)

        # Mostra os dados
        st.data_editor(filtro_dados, use_container_width=True)



        
        # Estilo do buttom de dawnload
        st.markdown("""
        <style>
        .stDownloadButton button {
            color: texto !important;
            #background-color:  #586e75!important;
        }
        </style>
        """, unsafe_allow_html=True)


        col1, col2, col3 = st.columns([3,1,1])
        
        with col1:
            
            csv = filtro_dados.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
            st.download_button(
                label="⬇️ Baixar CSV",
                data=csv,
                file_name='unidades_ensino_recife.csv',
                mime='text/csv',
                
            )
        with col2:
            totalLinhas = filtro_dados.shape[0]
            st.metric("📄 Total de Linhas", value=totalLinhas, border=True)

        with col3:
            totalColunas = filtro_dados.shape[1]
            st.metric("📊 Total de Colunas", value=totalColunas, border=True)
    else:
        st.dataframe(df_filtrado)


def mainDataframe(df):
    divisor()
    dataframe(df)
    divisor()