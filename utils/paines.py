# utils/dashboards.py
import streamlit as st
#import folium
#from streamlit_folium import st_folium
#from folium.plugins import MarkerCluster
from streamlit_option_menu import option_menu
from utils.marcadores import divisor
from utils.graficos import (grafico_barra, grafico_pizza, grafico_scater, grafico_coluna, grafico_linha,  
                            grafico_heatmap, grafico_barra_sem_ordenar, grafico_radar)
from utils.filtros import filtros_aplicados, filtro_mes_nome
from utils.totalizadores import (total_acidentes,formatar_milhar, total_mortos, total_feridos, total_veiculos,
                                 calculo_tot_acidentes, calculo_tot_mortos, calculo_tot_feridos, calculo_tot_veiculos)

def graficos(df, df_original):

    aba1, aba2, aba3, aba4, aba5, aba6, aba7 = st.tabs(["📊 Quantitativos ","📉 Correlações", "📍 Localidades", "⚠️ Características dos Acidentes",
                                                  "⚡Fatores de Ocorrências",  "🗺️ Mapas", "🧹 Notas Explicativas" ])
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
        divisor()
        tot_mortos = calculo_tot_mortos(df)
        tot_feridos = calculo_tot_feridos(df)
        tot_veiculos = calculo_tot_veiculos(df)
        tot_acidentes = calculo_tot_acidentes(df)

        taxa_mortalidade = round((tot_mortos / tot_acidentes) * 100 if total_acidentes else 0,0)
        taxa_mortalidade_feridos = round((tot_mortos / tot_feridos) * 100 if total_feridos else 0, 0)
        media_veiculos_acidente = round(tot_veiculos / tot_acidentes if total_acidentes else 0, 0)

        c2, c3, c4 = st.columns(3)
        

        with c2.container(border=True):   
            st.metric("⚖️ Mortalidade (%)", f"{taxa_mortalidade:.2f}%")

        with c3.container(border=True):
            st.metric("🩸 Mortos / 100 Feridos", f"{taxa_mortalidade_feridos:.2f}%")

        with c4.container(border=True):
            st.metric("🚙 Veículos / Acidente", f"{media_veiculos_acidente:.2f}")  

        divisor()

        # Agrupar os dados por grupo de causa
        df_grouped = df.groupby("Causa Grupo", as_index=False).agg({
            "Feridos": "sum",
            "Mortos": "sum",
            "Veiculos": "sum"
        })
        # === GRÁFICO ===
        grafico_scater(
            "### 📉 Relação entre Feridos e Mortos (agrupado por causa)",
            df_grouped,
            coluna_x="Feridos",
            coluna_y="Mortos",
            tamanho_y="Veiculos",
            cor_bola="Causa Grupo",
            nome_bola="Causa Grupo",
            titulo="Correlação entre Feridos e Mortos por Grupo de Causa",
            key="grafico_feridos_mortos_causa"
        )


        divisor()
        # Agrupa os dados por tipo de acidente
        df_grouped_tipo = df.groupby("Tipo Acidente", as_index=False).agg({
            "Feridos": "sum",
            "Veiculos": "sum"
        })
        
        grafico_scater(
        "### 🚘 Relação entre Veículos e Feridos (agrupado por tipo de acidente)",
        df_grouped_tipo,
        coluna_x="Veiculos",
        coluna_y="Feridos",
        tamanho_y="Feridos",
        cor_bola="Tipo Acidente",
        nome_bola="Tipo Acidente",
        titulo="Correlação entre Veículos e Feridos por Tipo de Acidente",
        key="grafico_veiculos_feridos_tipo"
        )


    with aba3:                                                    
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
            top_n = st.slider("Top N Causa Acidente", min_value=5, max_value=8, value=5)
            grafico_barra(df, 'Causa Grupo', titulo="Causas de Acidentes",  top_n=top_n)
        #top_n = st.slider("Top N Estados", min_value=5, max_value=16, value=5)
        divisor()
        c3, c4 = st.columns(2)
        with c3:
            grafico_coluna(df, 'Condicao Climatica Grupo', titulo="Condicao Metereologica")
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

    
    
    with aba6:
        st.header("Análise Geográfica de Acidentes")

        c1, c2 = st.columns(2)
        with c1:
           df = filtros_aplicados(df, 'Br') 
        with c2:
           df = filtros_aplicados(df, 'Km')
        

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

    with aba7:
        
        st.header("📘 Metodologia da Análise")
        st.markdown("Abaixo estão os principais critérios e tratamentos aplicados aos dados utilizados neste painel:")

        with st.expander("🧹 **Tratamentos aplicados aos dados**"):
            st.markdown("""
            - Exclusão de registros **sem mortos e feridos** (mantidos apenas acidentes com vítimas);  
            - Junção das colunas **Feridos Graves** e **Feridos Leves** em `Feridos`;  
            - Remoção da coluna `Ilesos`, por não representar gravidade no evento;  
            - Padronização de textos (nomes de municípios, causas, condições climáticas, etc.);  
            - Junção das colunas `Município` e `UF` → `Município - UF`.  
            """)

        with st.expander("🧠 **Agrupamento das causas dos acidentes**"):
            st.markdown("""
            - 🚗 **Condutor - Falha humana:** Reação tardia, contramão, ultrapassagem, velocidade, celular, etc.  
            - 💤 **Condutor - Fadiga / Álcool / Drogas / Saúde:** Sono, ingestão de álcool, mal súbito.  
            - 🛣️ **Via / Infraestrutura:** Buracos, pista escorregadia, sinalização deficiente, iluminação ruim.  
            - 🌧️ **Clima / Ambiente:** Chuva, neblina, fumaça, óleo, areia.  
            - 🔧 **Veículo - Falha mecânica:** Freios, suspensão, pneus, faróis.  
            - 🚶 **Pedestre:** Travessia fora da faixa, embriaguez, falta de passarela.  
            - 🐄 **Animais / Objetos / Obstáculos:** Animais, objetos, obstruções.  
            - ❓ **Outros / Indefinidos:** Causas não especificadas.  
            """)

        with st.expander("📆 **Período e fonte dos dados**"):
            st.markdown("""
            - Dados públicos da **Polícia Rodoviária Federal (PRF)**.  
            - Período analisado: **2023 e 2024**.  
            - Escopo: acidentes com vítimas (mortos e/ou feridos).  
            """)

        with st.expander("💡 **Objetivo da aplicação**"):
            st.markdown("""
            Este painel interativo foi desenvolvido para **explorar os padrões e fatores associados aos acidentes rodoviários**, 
            permitindo identificar relações entre causas, condições climáticas, horários e gravidade dos eventos.
            """)

        st.markdown("---")
        st.caption("_Esta aba tem como objetivo garantir transparência e reprodutibilidade da análise._")



def mainGraficos(df, df_original):
    divisor()
    # df_filtrado e o df_filtrado_linha para a função graficos e df para valores preditivos para evitar ação de filtros nas variáveis
    graficos(df, df_original) 
    #divisor()