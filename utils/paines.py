# utils/dashboards.py
import streamlit as st
#import folium
#from streamlit_folium import st_folium
#from folium.plugins import MarkerCluster
from streamlit_option_menu import option_menu
from utils.marcadores import divisor
from utils.graficos import grafico_barra, grafico_pizza, grafico_treemap, grafico_coluna
from utils.filtros import filtros_aplicados, filtro_mes_nome


def graficos(df):

    aba1, aba2, aba3, aba4, aba5 = st.tabs(["📊 Quantitativos ", "🚗 Localidades", "🛣️ Características dos Acidentes", 
                                      "Infraestrutura Viária", "mapas"])
    divisor()
    with aba1:                                                    
    
        c1, c2 = st.columns(2)
        with c1:
            grafico_barra(df, 'Ano', None, titulo="Acidentes")        # conta linhas
        with c2:
            grafico_barra(df, 'Ano', 'Mortos', titulo="Mortes")       # soma a coluna Mortos

        c3, c4 = st.columns(2)
        with c3:
            grafico_barra(df, 'Ano', 'Feridos', titulo="Feridos")    # soma a coluna Feridos
        with c4:
            grafico_barra(df, 'Ano', 'Veiculos', titulo="Veículos")  # soma a coluna Veículos 

    with aba2:                                                    
        c1, c2, c3 = st.columns(3)
        with c1:
           df = filtros_aplicados(df, 'Classificacao Acidente') 
        with c2:
           df = filtros_aplicados(df, 'Partes Dia')
        with c3:
            df = filtros_aplicados(df, 'Condicao Metereologica')
        
        divisor()

        grafico_barra(df, 'Região', coluna_y=None, titulo="Acidentes por Região")
        top_n = st.slider("Top N Estados", min_value=5, max_value=27, value=10)
        grafico_barra(df, 'Estado', titulo="Acidentes por Estados", top_n=top_n)
        top_n = st.slider("Top N Municípios", min_value=5, max_value=30, value=10)
        grafico_barra(df, 'Municipio', titulo="Acidentes por Municípios - Top 20", top_n=top_n)

    with aba3:
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
            grafico_treemap(df, 'Partes Dia', titulo="Partes Dia")

    with aba4:
        c1, c2 = st.columns(2)
        with c1:
            grafico_treemap(df, 'Tipo Pista', titulo="Tipo Pista")
        with c2:
            grafico_pizza(df, 'Uso Solo', titulo="Trecho Urbano ou Rural")
        divisor()
        c3,c4 = st.columns(2)
        with c3:
            grafico_barra(df, 'Grupo Via', titulo="Tracado Via")
        with c4:
            top_n = st.slider("Top N BR", min_value=5, max_value=20, value=5)
            grafico_barra(df, 'Br', titulo="Top 20 BR mais acidentes", top_n=top_n)

    
    with aba5:
        st.header("Em construção!!!")
        '''
        st.subheader("Mapa Interativo de Acidentes")

        # --- Substitua 'latitude' e 'longitude' pelos nomes reais das colunas no seu DF ---
        if 'Latitude' not in df.columns or 'Longitude' not in df.columns:
            st.error("Erro: O DataFrame não contém as colunas 'Latitude' e 'Longitude' para plotar o mapa.")
            st.dataframe(df.columns) # Mostra as colunas disponíveis
        
        else:
            # Remover linhas onde lat/lon são nulos, se houver
            df_mapa = df.dropna(subset=['Latitude', 'Longitude'])

            # 1. Criar um mapa Folium básico
            m = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)

            # 2. Criar um MarkerCluster
            # Isso agrupa os pontos próximos para melhor performance e visualização
            marker_cluster = MarkerCluster().add_to(m)

            # AVISO: Se o seu DataFrame for MUITO grande (ex: +50.000 linhas),
            # o mapa pode demorar para carregar.
            # Considere usar uma amostra, como:
            # if len(df_mapa) > 50000:
            #     df_mapa = df_mapa.sample(50000)
            #     st.warning("Exibindo uma amostra de 50.000 acidentes para melhor performance.")


            # 3. Adicionar cada acidente (linha do df) ao cluster
            for _, row in df_mapa.iterrows():
                
                # Crie um texto para o Popup (o que aparece ao clicar)
                # Use .get() para evitar erros se a coluna não existir
                popup_text = f"<strong>Tipo:</strong> {row.get('Tipo Acidente', 'N/A')}<br>" \
                             f"<strong>Mortos:</strong> {int(row.get('Mortos', 0))}<br>" \
                             f"<strong>Feridos:</strong> {int(row.get('Feridos', 0))}<br>" \
                             f"<strong>Data:</strong> {row.get('Data', 'N/A')}" # Assumindo que você tem uma coluna 'Data'

                folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    # Tooltip é o que aparece ao passar o mouse
                    tooltip=row.get('Tipo Acidente', 'Clique para detalhes'), 
                    # Popup é o que aparece ao clicar
                    popup=folium.Popup(popup_text, max_width=300),
                ).add_to(marker_cluster)

            # 4. Renderizar o mapa no Streamlit
            st.subheader("Mapa de Acidentes")
            # Use 'width="100%"' para ocupar o espaço da aba
            output = st_folium(m, width="100%", height=600)

            # 5. (Opcional) Mostrar dados de interação
            with st.expander("Ver dados de interação do mapa (para debug)"):
                st.write(output)
    '''


def mainGraficos(df):
    divisor()
    # df_filtrado e o df_filtrado_linha para a função graficos e df para valores preditivos para evitar ação de filtros nas variáveis
    graficos(df) 
    divisor()