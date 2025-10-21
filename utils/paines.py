# utils/dashboards.py
import streamlit as st
#import folium
#from streamlit_folium import st_folium
#from folium.plugins import MarkerCluster
from streamlit_option_menu import option_menu
from utils.marcadores import divisor
from utils.graficos import grafico_barra, grafico_pizza, grafico_treemap, grafico_coluna, grafico_linha,  grafico_heatmap, grafico_barra_sem_ordenar, grafico_radar
from utils.filtros import filtros_aplicados, filtro_mes_nome
from utils.totalizadores import total_acidentes,formatar_milhar, total_mortos, total_feridos, total_veiculos

def graficos(df, df_original):

    aba1, aba2, aba3, aba4, aba5 = st.tabs(["📊 Quantitativos ", "📍 Localidades", "⚡Fatores de Ocorrências",
                                            "⚠️ Características dos Acidentes",  "🗺️ Mapas"])
    divisor()
    with aba1:
        c1, c2 = st.columns([3,2])
        with c1:
            grafico_linha(df, 'Data Inversa', None, titulo="Acidentes por Ano/Mês")
        with c2:
            grafico_barra_sem_ordenar(df, 'Ano', titulo=f"Acidentes = {total_acidentes(df)}")
        
        c3, c4 = st.columns([3,2])
        with c3:
            grafico_linha(df, 'Data Inversa', 'Mortos', titulo="Mortos por Ano/Mês")
        with c4:
            grafico_barra_sem_ordenar(df, 'Ano', 'Mortos', titulo=f"Mortos = {total_mortos(df)}")

        c5, c6 = st.columns([3,2])
        with c5:
            grafico_linha(df, 'Data Inversa', 'Feridos', titulo="Feridos por Ano/Mês")
        with c6:
            grafico_barra_sem_ordenar(df, 'Ano','Feridos', titulo=f"Feridos = {total_feridos(df)}")
        c7, c8 = st.columns([3,2])
        with c7:
            grafico_linha(df, 'Data Inversa', 'Veiculos', titulo="Veículos por Ano/Mês")
        with c8:
            grafico_barra_sem_ordenar(df,'Ano', 'Veiculos', titulo=f"Veículos = {total_veiculos(df)}")
        c9, c10 = st.columns([3,2])
        with c9:
            grafico_linha(df, 'Dia Semana', 'Veiculos', titulo="Veículos por Dia da Semana")
        with c10:
            grafico_barra_sem_ordenar(df,'Dia Semana', 'Veiculos', titulo=f"Dia da semana = {total_veiculos(df)}")
        
  
    with aba2:                                                    
        c1, c2, c3 = st.columns(3)
        with c1:
           df = filtros_aplicados(df, 'Classificacao Acidente') 
        with c2:
           df = filtros_aplicados(df, 'Fase Dia')
        with c3:
            df = filtros_aplicados(df, 'Condicao Metereologica')
        
        
        divisor()

        grafico_barra(df, 'Região', coluna_y=None, titulo="Acidentes por Região")
        top_n = st.slider("Top N Estados", min_value=5, max_value=27, value=10)
        grafico_barra(df, 'Uf', titulo="Acidentes por Estados", top_n=top_n)
        top_n = st.slider("Top N Municípios", min_value=5, max_value=30, value=10)
        grafico_barra(df, 'Municipio', titulo="Acidentes por Municípios - Top 20", top_n=top_n)
        top_n = st.slider("Top N BR", min_value=5, max_value=30, value=5)
        grafico_barra(df, 'Br', titulo="Top 20 BR mais acidentes", top_n=top_n)
        


    with aba4:
        '''
        c7, c8, c9 = st.columns(3)
        with c7:
           df = filtros_aplicados(df, 'Classificacao Acidente') 
        with c8:
           df = filtros_aplicados(df, 'Partes Dia')
        with c9:
            df = filtros_aplicados(df, 'Condicao Metereologica')

        divisor()
        '''
        c1, c2 = st.columns(2)
        with c1:
            top_n = st.slider("Top N Tipo Acidente", min_value=5, max_value=16, value=5)
            grafico_barra(df, 'Tipo Acidente', titulo="Tipos de Acidentes",  top_n=top_n)
        with c2:
            top_n = st.slider("Top N Causa Acidente", min_value=5, max_value=30, value=5)
            grafico_barra(df, 'Causa Acidente', titulo="Causas de Acidentes",  top_n=top_n)
        #top_n = st.slider("Top N Estados", min_value=5, max_value=16, value=5)
        divisor()
        c3, c4 = st.columns(2)
        with c3:
            grafico_coluna(df, 'Condicao Metereologica', titulo="Condicao Metereologica")
        with c4:
            #grafico_barra(df, 'Grupo Via', titulo="Tracado Via")
            grafico_barra(df, 'Fase Dia', titulo="Fase do Dia")

        divisor()
        st.subheader("🎯 Selecione parâmetros abaixo para construção de um gráfico de radar para analise")
        # Grafico de radar interativo
        # Dando opcoes para o usuario escolher
        colunas_categoricas = ['Condicao Metereologica', 'Fase Dia', 'Tipo Acidente', 'Classificacao Acidente',
                               'Grupo Via', 'Região', 'Uf']
        colunas_numericas = ['Ano', 'Mês', 'Mortos', 'Feridos', 'Veiculos', 'Dia Da Semana']

        # Filtro para categoria (eixo angular)
        coluna_categoria = st.selectbox(
            "Escolha a categoria (eixo angular)", 
            options=colunas_categoricas, 
            index=colunas_categoricas.index("Tipo Acidente") if "Tipo Acidente" in colunas_categoricas else 0
        )

        # Filtro para grupo (ex.: Ano)
        coluna_grupo = st.selectbox(
            "Escolha o grupo para comparar (cor)", 
            options=[None] + colunas_numericas, 
            index=colunas_numericas.index("Ano") + 1 if "Ano" in colunas_numericas else 0
        )

        
        # Validação e chamada do gráfico
       
        if coluna_categoria == coluna_grupo:
            st.warning("⚠️ As colunas de categoria e grupo não podem ser iguais. Escolha colunas diferentes.")
        else:
            try:
                grafico_radar(df, coluna_categoria, coluna_grupo, f"{coluna_categoria} x {coluna_grupo if coluna_grupo else ''}")
            except Exception as e:
                st.error(f"Erro ao gerar o gráfico de radar: {e}")

                
        
        
    with aba3:
                  
        #df = filtros_aplicados(df, 'Km') 
        #df = filtros_aplicados(df, 'Br')

        divisor()

        c1, c2 = st.columns(2)
        with c1:
            grafico_coluna(df, 'Tipo Pista', titulo="Tipo Pista")
        with c2:
            grafico_pizza(df, 'Uso Solo', titulo="Trecho Urbano ou Rural")
        divisor()
        c3, c4 = st.columns(2)     
        with c3:
            grafico_barra(df, 'Dia Semana', titulo="Dia da Semana")
        with c4:
            grafico_coluna(df, 'Fase Dia', titulo="Fase do Dia")
        
        #grafico_radar(df, 'Grupo Via', 'Ano', 'Vias com maior indice de acidentes')
        #grafico_radar(df, 'Classificacao Acidente', 'Ano', 'Vias com maior consequencia nos acidentes')
        #grafico_radar(df, 'Condicao Metereologica', 'Mortos', 'Condição meterológica com maior consequencia nos acidentes')
    
    with aba5:
        st.header("Análise Geográfica de Acidentes")

        # Seletor de tipo de mapa
        tipo_mapa = st.radio(
            "Escolha o indicador para visualizar:",
            ["Mortes", "Feridos", "Acidentes"],
            horizontal=True
        )

        # Define qual coluna e título usar
        if tipo_mapa == "Mortes":
            coluna_valor = "Mortos"
            titulo = "Mapa de Calor - Mortes em Rodovias Federais"
        elif tipo_mapa == "Feridos":
            coluna_valor = "Feridos"
            titulo = "Mapa de Calor - Feridos em Rodovias Federais"
        else:
            coluna_valor = "Veiculos"
            titulo = "Mapa de Calor - Total de Acidentes (por veículos envolvidos)"

        # Gera o gráfico
        fig = grafico_heatmap(df, coluna_valor, titulo)

        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não foi possível gerar o mapa. Verifique se há dados válidos.")
                

def mainGraficos(df, df_original):
    divisor()
    # df_filtrado e o df_filtrado_linha para a função graficos e df para valores preditivos para evitar ação de filtros nas variáveis
    graficos(df, df_original) 
    #divisor()