import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from utils.marcadores import divisor
from utils.graficos import (grafico_barra, grafico_pizza, grafico_scater,  grafico_linha,  
                            grafico_heatmap, grafico_radar, grafico_treemap, grafico_coluna)
from utils.filtros import filtros_aplicados
from utils.totalizadores import (total_acidentes,formatar_milhar, total_mortos, total_feridos, total_veiculos,
                                 calculo_tot_acidentes, calculo_tot_mortos, calculo_tot_feridos, calculo_tot_veiculos)




# Funcao para escolher a coluna categorica precisa de chave 
def escolher_coluna_categorica(colunas_categoricas, chave):
    
    return st.selectbox(
                "Selecione a escala de tempo disponivel do conjunto de dados para o Eixo X",
                options=colunas_categoricas,
                key=chave
            )

def escolher_coluna_numerica(grupo_options_display, chave):
    return st.selectbox(
                "Selecione o grupo disponivel do conjunto de dados para o Eixo Y)",
                options=grupo_options_display,
                #index=0,
                key=chave
            )



def graficos(df):

    aba1, aba2, aba3, aba4, aba5, aba6, aba7 = st.tabs(["⏳ Linha do Tempo ","📉 Analise relacional", "🌍 Distribuição Geográfica", "⚠️ Características dos Acidentes",
                                                  "⚡Fatores de Ocorrências",  "🗺️ Mapas", "🧹 Notas Explicativas" ])
    divisor()
    with aba1:
          
                
        st.subheader("🎯 Selecione parâmetros abaixo para construção de um gráfico temporal para análise")

        #  Definição de colunas 
        colunas_categoricas = ['Data', 'Ano', 'Mês', 'Dia', 'Dia Semana', 'Hora']
        colunas_numericas = ['Mortos', 'Feridos', 'Veiculos']

        # Calculo coluna numericas e o none para somatario do df
        grupo_display_map = [("Total Acidentes", None)] + [(col, col) for col in colunas_numericas]
        grupo_options_display = [g[0] for g in grupo_display_map]


        c1,c2 = st.columns(2, gap="large")
        with c1:
            #  Selectbox para categoria (Eixo X) com a chave que sera qtd de vez repetida
            coluna_categoria = escolher_coluna_categorica(colunas_categoricas, 'primeiracategoria')
        with c2:
            #  Selectbox para grupo (Eixo Y) 
            # Mapeando None para "Total Acidentes"
            coluna_grupo_display = escolher_coluna_numerica(grupo_options_display, 'primeiranumerica')

        # Recupera o valor real do selectbox
        coluna_grupo = dict(grupo_display_map)[coluna_grupo_display]

        #  Validação de categoria e grupo iguais 
        if coluna_categoria == coluna_grupo:
            st.warning("⚠️ As colunas de categoria e grupo não podem ser iguais. Escolha colunas diferentes.")
            st.stop()

        #  Preparação para gráfico 
        df_temp = df.copy()

        # Ordenar mês corretamente, caso seja selecionado
        if coluna_categoria == "Mês":
            meses_pt = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
            df_temp['Mês'] = pd.Categorical(df_temp['Mês'], categories=meses_pt, ordered=True)
            
        # Ordenar dia da semana corretamente, caso seja selecionado
        if coluna_categoria == "Dia Semana":
            dias_semana = ["Domingo", "Segunda-Feira", "Terça-Feira", "Quarta-Feira",
                        "Quinta-Feira", "Sexta-Feira", "Sábado"]
            df_temp['Dia Semana'] = pd.Categorical(df_temp['Dia Semana'], categories=dias_semana, ordered=True)

        #  Título dinâmico 
        titulo = f"📊 {coluna_grupo_display} por {coluna_categoria}"

        #  Chamada do gráfico de linha 
        try:
            grafico_linha(df_temp, coluna_categoria, coluna_grupo, titulo)
        except Exception as e:
            st.error(f"Erro ao gerar o gráfico de linha: {e}")

                

    with aba2:
        divisor()
        tot_mortos = calculo_tot_mortos(df)
        tot_feridos = calculo_tot_feridos(df)
        tot_veiculos = calculo_tot_veiculos(df)
        tot_acidentes = calculo_tot_acidentes(df)

        taxa_mortalidade = round((tot_mortos / tot_acidentes) * 100 if total_acidentes else 0,0)
        taxa_mortalidade_feridos = round((tot_mortos / tot_feridos) * 100 if total_feridos else 0, 0)
        media_veiculos_acidente = round(tot_veiculos / tot_acidentes if total_acidentes else 0, 0)

        st.subheader("🔍 Estatísticas")
        c2, c3, c4 = st.columns(3, gap="large")
        
        with c2.container(border=True):   
            st.metric("⚖️ Mortalidade (Mortos/Acidentes)", f"{taxa_mortalidade:g}%")

        with c3.container(border=True):
            st.metric("🩸 Mortos / 100 Feridos", f"{taxa_mortalidade_feridos:g}%")

        with c4.container(border=True):
            st.metric("🚙 Veículos / Acidente", f"{media_veiculos_acidente:g}")  

        divisor()

        st.subheader('🚗💥 Causas x Consequências dos Acidentes')
        st.subheader('🧭 Selecione os parâmetros e o fator de análise para construção de gráficos relacionais.')


        #  Definição de colunas 
        colunas_x = ['Feridos', 'Mortos', 'Veiculos', 'Feridos Leves', 'Feridos Graves']
        coluna_causa = ['Grupo Via', 'Condicao Climatica Grupo', 'Tipo Acidente', 'Causa Grupo', 'Tipo Pista',
                        'Dia Semana', 'Partes Dia', 'Ano', 'Mês', 'Dia','Hora']

        c1,  c3 = st.columns(2, gap="large")

        with c1:
            opcoes = st.multiselect(
                "⚠️ Selecione duas variáveis para gerar o gráfico",
                options=colunas_x,
                max_selections=2, 
                default=["Feridos", "Mortos"],
                key="select_coluna_x"
            )
           
        with c3:
            causa = st.selectbox(
                "🎯 Selecione o fator de análise (ex: Região, Tipo, Causa, etc.)",
                options=coluna_causa,
                key="select_causa"
            )
        
        #Verificação de variáveis iguais 
        # Verifica se o usuário escolheu 2 variáveis
        if len(opcoes) < 2:
            st.warning("⚠️ Selecione duas variáveis para gerar o gráfico.")
            st.stop()  # interrompe a execução do restante do código até que o usuário selecione 2
        else:
            coluna_x, coluna_y = opcoes[0], opcoes[1]

        
        coluna_x = opcoes[0]
        coluna_y = opcoes[1]
        #  Preparação para gráfico 
        df_temp = df.copy()

        #  Título dinâmico 
        titulo = f"📊 {coluna_x} por {coluna_y}"

        #  Agrupa os dados pela causa selecionada 
        df_grouped_tipo = df.groupby(causa, as_index=False).agg({
            coluna_x: "sum",
            coluna_y: "sum"
        })

        #  Gera o gráfico 
        grafico_scater(
            df_grouped_tipo,
            coluna_x=coluna_x,
            coluna_y=coluna_y,
            tamanho_y=coluna_y,
            cor_bola=causa,         #  causa selecionada, não a lista
            nome_bola=causa,        #  causa selecionada, não a lista
            titulo=f"Relação entre {coluna_x} e {coluna_y} por {causa}",
            key="grafico_mortos_feridos"
        )


    with aba3:
        st.subheader('🧩 Filtros Extras')                                            
        c1, c2, c3 = st.columns(3, gap="large")
        with c1:
           df = filtros_aplicados(df, 'Classificacao Acidente') 
        with c2:
           df = filtros_aplicados(df, 'Fase Dia')
        with c3:
            df = filtros_aplicados(df, 'Condicao Metereologica')
        
        
        divisor()
        
        st.subheader("🎯 Selecione os parâmetros e o fator de análise para construção de gráficos.")
        

        #  Definição de colunas 
        colunas_categoricas = ['Região', 'Uf', 'Municipio', 'Br']
        colunas_numericas = ['Mortos', 'Feridos', 'Veiculos']

        c1, c2 = st.columns(2, gap="large")

        with c1:
            coluna_categoria = escolher_coluna_categorica(colunas_categoricas, 'segundaCategoria')

        with c2:
            grupo_display_map = [("Total Acidentes", None)] + [(col, col) for col in colunas_numericas]
            grupo_options_display = [g[0] for g in grupo_display_map]

            coluna_grupo_display = escolher_coluna_numerica(grupo_options_display, 'segundaNumerica')

                #  Mapeia o nome exibido (display) para o valor real 
            mapa_display_para_valor = dict(grupo_display_map)
            coluna_grupo = mapa_display_para_valor[coluna_grupo_display]

            #  Preparação para gráfico 
            df_temp = df.copy()

            #  Título dinâmico 
            titulo = f"📊 {coluna_grupo_display} por {coluna_categoria}"

        # Seletor de tipo de gráfico
        st.subheader("📊 Escolha o tipo de gráfico")
        tipo_mapa = st.radio(
            "",
            ["Treemap", "Barra", "Coluna" ],
            horizontal=True
        )
            

        #  Chamada do gráfico de barras 
        if tipo_mapa == "Treemap": 
            try:
                if coluna_categoria != "Região":
                    top_n = st.slider(
                    "Top N para Estados, Municípios e Brs - no máximo 30",
                    min_value=5,
                    max_value=30,
                    value=5
                )
                else:
                    top_n = 5  # só 5 regiões, não precisa do slider

                grafico_treemap(df_temp, coluna_categoria, coluna_grupo, titulo, top_n=top_n)
            except Exception as e:
                st.error(f"Erro ao gerar o gráfico de barras: {e}")
        elif  tipo_mapa == "Barra":
            try:
                if coluna_categoria != "Região":
                    top_n = st.slider(
                    "Top N para Estados, Municípios e Brs - no máximo 30",
                    min_value=5,
                    max_value=30,
                    value=5
                )
                else:
                    top_n = 5  # só 5 regiões, não precisa do slider

                grafico_barra(df_temp, coluna_categoria, coluna_grupo, titulo, top_n=top_n)
            except Exception as e:
                st.error(f"Erro ao gerar o gráfico de barras: {e}")
        else:
            try:
                if coluna_categoria != "Região":
                    top_n = st.slider(
                    "Top N para Estados, Municípios e Brs - no máximo 30",
                    min_value=5,
                    max_value=30,
                    value=5
                )
                else:
                    top_n = 5  # só 5 regiões, não precisa do slider

                grafico_coluna(df_temp, coluna_categoria, coluna_grupo, titulo, top_n=top_n)
            except Exception as e:
                st.error(f"Erro ao gerar o gráfico de barras: {e}")
        
    with aba4:
        
        divisor()
        
        st.subheader("🎯 Selecione os parâmetros e o fator de análise para construção de gráficos.")
    
        
        # As variáveis disponíveis
        colunas_categoricas = ['Tipo Pista', 'Condicao Climatica Grupo', 'Fase Dia', 'Partes Dia']
        colunas_numericas = ['Mortos', 'Feridos', 'Veiculos']

        c1, c2 = st.columns(2, gap="large")

        # Receber as variáveis dos gráficos
        with c1:
            coluna_categoria = escolher_coluna_categorica(colunas_categoricas, "terceiraCategoria")
        with c2:
            grupo_display_map = [("Total Acidentes", None)] + [(col, col) for col in colunas_numericas]
            grupo_options_display = [g[0] for g in grupo_display_map]

            coluna_grupo_display = escolher_coluna_numerica(grupo_options_display, 'terceiraNumerica')

                # Mapeia o nome exibido (display) para o valor real 
            mapa_display_para_valor = dict(grupo_display_map)
            coluna_grupo = mapa_display_para_valor[coluna_grupo_display]

            #  Preparação para gráfico 
            df_temp = df.copy()

            #  Título dinâmico 
            titulo = f"📊 {coluna_grupo_display} por {coluna_categoria}"

        # Seletor de tipo de gráfico
        st.subheader("📊 Escolha o tipo de gráfico")
        # Seletor de tipo de gráfico
        tipo_mapa = st.radio(
            "",
            ["Treemap", "Pizza", "Coluna"],
            horizontal=True
        )

        # Exibir os gráficos 
        if tipo_mapa == "Treemap":
            try:
                grafico_treemap(df_temp, coluna_categoria, coluna_grupo, titulo, top_n=top_n)
            except Exception as e:
                st.error(f"Erro ao gerar o gráfico de treemap: {e}")
        elif tipo_mapa == "Pizza":
            try:
                grafico_pizza(df_temp, coluna_categoria, coluna_grupo, titulo, top_n=top_n)
            except Exception as e:
                st.error(f"Erro ao gerar o gráfico de treemap: {e}")
        else:
            try:
                grafico_coluna(df_temp, coluna_categoria, coluna_grupo, titulo, top_n=top_n)
            except Exception as e:
                st.error(f"Erro ao gerar o gráfico de treemap: {e}")
    

    with aba5:
        
        divisor()
        st.subheader("🎯 Selecione parâmetros abaixo para construção de um gráfico de radar para análise")
        # Grafico de radar interativo
        # Dando opcoes para o usuario escolher
        colunas_categoricas = ['Condicao Metereologica', 'Fase Dia', 'Tipo Acidente', 'Classificacao Acidente',
                               'Grupo Via', 'Região', 'Uf', 'Partes Dia', 'Causa Grupo', 'Condicao Climatica Grupo']
        colunas_numericas = ['Ano', 'Mês', 'Mortos', 'Feridos', 'Veiculos', 'Dia Semana']

        # Filtro para categoria (eixo angular)
        coluna_categoria = escolher_coluna_categorica(colunas_categoricas, 'Quartavez')

        # Filtro para grupo (ex.: Ano) - Aqui já é diferente de categorias numericas
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
                titulo = f"📊 {coluna_categoria} por {coluna_grupo if coluna_grupo else ''}"
                grafico_radar(df, coluna_categoria, coluna_grupo, titulo)
            except Exception as e:
                st.error(f"Erro ao gerar o gráfico de radar: {e}")

    
    
    with aba6:
        
        st.subheader("🎯 Selecione parâmetros abaixo para construção de um mapa de calor dinâmico")

        #  Cópia temporária do dataframe 
        df_temp = df.copy()

        #  Seletor de tipo de mapa 
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

        #  Slider para reduzir a quantidade de pontos 
        top_n = st.slider(
            "Selecione o número de BRs para exibir (5 a 15):",
            min_value=5,
            max_value=15,
            value=10
        )

        try:
            #  Ordena e filtra as BRs com mais ocorrências 
            if "Br" in df_temp.columns and coluna_valor in df_temp.columns:
                top_brs = (
                    df_temp.groupby("Br")[coluna_valor]
                    .sum()
                    .nlargest(top_n)
                    .index
                )
                df_temp = df_temp[df_temp["Br"].isin(top_brs)]

            #  Chama a função de mapa de calor 
            fig = grafico_heatmap(df_temp, coluna_valor, titulo)
            if fig is not None:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Não há dados suficientes para gerar o mapa.")
        except Exception as e:
            st.error(f"Erro ao gerar o mapa de calor: {e}")

    with aba7:
        
        # Fazer nota explicatoria da analise de dados e desenvolvimento do app

        st.header("📘 Metodologia da Análise")
        st.markdown("Abaixo estão os principais critérios e tratamentos aplicados aos dados utilizados neste painel:")

        with st.expander("📢 **Construção de Gráficos**"):
            st.markdown("""
            - ⚙️ O aplicativo permite a **escolha de diversos parâmetros** para personalizar suas análises;  
            - 📊 Selecione os **gráficos** que melhor representem as informações que deseja explorar;  
            - 🔍 Experimente diferentes combinações para obter **novas perspectivas** sobre os dados.  
            """)

        with st.expander("🧹 **Principais tratamentos aplicados aos dados/Enriquecimento da fonte de dados**"):
            st.markdown("""
            - Junção das colunas **Feridos Graves** e **Feridos Leves** em `Feridos`;  
            - Criação das colunas ['Ano', 'Mês','Dia', 'Hora', 'Partes_Dia', 'Região'] para futura aplicação de machine learning 
                        e descendo a granularidade de tempo;  
            - Junção das colunas `Município` e `UF` → `Município - UF`.
            """)

        with st.expander("🧠 **Agrupamento da coluna 'Causas_Acidentes**"):
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

        with st.expander("⏰ **Agrupamento da coluna 'Partes Dia'**"):
            st.markdown("""
            - 🌅 **06:00 às 11:59 - Manhã**  
            - 🌇 **12:00 às 17:59 - Tarde**  
            - 🌙 **18:00 às 23:59 - Noite**  
            - 🛌 **00:00 às 05:59 - Madrugada**  
            """)

        with st.expander("🧠 **Agrupamento da coluna 'Condicao_Metereologica'**"):
            st.markdown("""
            - ☀️ **Bom:** Céu claro, sol, nublado.   
            - 🌧️ **Chuva:** Chuva, garoa, chuvisco.  
            - 🌫️ **Outros:** Vento, nevoeiro, granizo, neve, ignorado.  
            """)  

        with st.expander("🛣️ **Agrupamento da coluna 'Grupo_via'**"):
            st.markdown("""
            - 🟢 **Reta:** Trechos retos da via.  
            - ↗️ **Aclive:** Trechos com subida acentuada.  
            - ↘️ **Declive:** Trechos com descida acentuada.  
            - 🔄 **Curva:** Trechos curvos da via, incluindo curvas fechadas e leves.  
            - 🏗️ **Viaduto:** Pontes, elevados ou viadutos.  
            - ❓ **Outros:** Qualquer outro tipo de trecho não classificado acima.  
            """)

        with st.expander("📆 **Período e fonte dos dados**"):
            st.markdown("""
            - Dados públicos da **Polícia Rodoviária Federal (PRF)**.  
            - Período analisado: **2021 a Ago/2025**.  
            - Escopo: acidentes com vítimas (mortos e/ou feridos), Veículos, Total de acidentes. 
            - Relatório anual de ocorrências 
            """)

        with st.expander("💡 **Objetivo da aplicação**"):
            st.markdown("""
            Este painel interativo foi desenvolvido para **explorar os padrões e fatores associados aos acidentes rodoviários**, 
            permitindo identificar relações entre causas, condições climáticas, horários e gravidade dos eventos.
            """)
        
        with st.expander("🛣️ Recomendações para Redução de Acidentes"):
            st.markdown("""


                Para reduzir a ocorrência de acidentes nas rodovias federais, recomenda-se a adoção das seguintes medidas:

                - 🚗 Campanhas institucionais voltadas à direção responsável, promovendo conscientização sobre comportamentos seguros no trânsito.  
                - 👮 Intensificação da fiscalização durante os períodos e locais de maior risco, garantindo maior presença e atuação preventiva das autoridades.  
                - ⚙️ Incentivo à adoção de tecnologias de segurança veicular, como:  
                     1) sistemas de frenagem automática;  
                     2) assistência à direção;  
                     3) outros recursos de segurança ativa.  
                **Nota:** O governo deveria incentivar — e até obrigar — as montadoras a produzirem esses sistemas em série para todos os veículos fabricados, 
                a exemplo do que foi feito com os cintos de segurança e o DRL (luz diurna).  
                - 🚧 Instalação de lombadas eletrônicas e outros mecanismos de controle de velocidade nos pontos com maior concentração de acidentes.  
                - 📢 Divulgação massiva dos dados de acidentes, promovendo transparência e conscientização da sociedade, 
                uma vez que a falta de informação também contribui para os altos índices de incidência nas rodovias federais.  
                - 🏥 Divulgação dos **custos de saúde pública** decorrentes dos acidentes, evidenciando o impacto financeiro e social desses eventos. 
                Tal transparência permitiria ao próprio governo **direcionar mais investimentos para ações preventivas do que reparadoras**, 
                reconhecendo que **uma vida não tem preço**.  

                A combinação dessas ações pode contribuir significativamente para reduzir o número de acidentes e aumentar a segurança viária nas rodovias federais.
            """, unsafe_allow_html=True)
                    

        st.markdown("---")
        st.caption("_Nosso objetivo garantir transparência e reprodutibilidade da análise._")



def mainGraficos(df):
    divisor()
    graficos(df) 
   