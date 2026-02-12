import streamlit as st
import altair as alt
import plotly.express as px
import pandas as pd
import numpy as np
from utils.totalizadores import formatar_milhar



def grafico_barra(df, coluna_x, coluna_y=None, titulo=None, top_n=None):
    

    # Subtítulo no Streamlit
    if titulo:
        st.subheader(titulo)

    # Preparação dos dados
    if coluna_y is None:
        total = df.groupby(coluna_x).size().reset_index(name='Total')
    else:
        total = df.groupby(coluna_x)[coluna_y].sum().reset_index(name='Total')

    # Limita categorias
    if top_n is not None:
        total = total.nlargest(top_n, 'Total')

    # Ordena para exibir barras em ordem decrescente
    total = total.sort_values('Total', ascending=False)
    total['Total_str'] = formatar_milhar(total['Total'])

    # Força eixo categórico a ser string
    total[coluna_x] = total[coluna_x].astype(str)
    # Calcula percentual
    soma_total = total['Total'].sum()
    total['Percentual'] = (total['Total'] / soma_total * 100).round(1) if soma_total else 0

    # Tema automático
    tema = 'plotly_white' if st.get_option("theme.base") == "light" else 'plotly_dark'

    # Criação do gráfico
    fig = px.bar(
        total,
        x=coluna_x,
        y='Total',
        text='Total_str',
        hover_data={'Percentual': True, 'Total': True}
    )

    # Ajustes visuais
    fig.update_traces(
        textposition='outside',  # rótulos acima das barras
        marker_color='#1f77b4'
    )
    fig.update_layout(
        template=tema,
        yaxis=dict(title=None, showticklabels=False),
        xaxis=dict(title=None, showticklabels=True, categoryorder='total descending'),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)



# Grafico de pizza

def grafico_pizza(df, coluna_categoria, coluna_valor=None, titulo=None, top_n=None):
   
    if titulo:
        st.subheader(titulo)

    # Agregação dos dados
    if coluna_valor is None:
        total = df.groupby(coluna_categoria).size().reset_index(name='Total')
    else:
        total = df.groupby(coluna_categoria)[coluna_valor].sum().reset_index(name='Total')

    # Limita as categorias
    if top_n is not None:
        total = total.nlargest(top_n, 'Total')

    # Tratamento de dataframe vazio
    if total.empty:
        st.warning(f"Não há dados para exibir no gráfico: {titulo or ''}")
        return

    # Calcula colunas para o Tooltip
    soma_geral = total['Total'].sum()
    total['Percentual'] = (total['Total'] / soma_geral * 100) if soma_geral > 0 else 0
    total['Total_str'] = total['Total'].apply(formatar_milhar)

    # Ordena
    total = total.sort_values('Total', ascending=False)
    
    # Tema
    tema = 'plotly_white' if st.get_option("theme.base") == "light" else 'plotly_dark'

<<<<<<< HEAD
    # Aplicando
=======
    # 7. Aplicando
>>>>>>> c92491a (Atualizando a base de dados - Ano 2025)
    fig = px.pie(
        total,
        names=coluna_categoria,    # As fatias
        values='Total_str',            # O tamanho
        color=coluna_categoria,    # Cor baseada NA CATEGORIA
        color_discrete_sequence=px.colors.sequential.Blues[2:], # Usa a paleta de azuis
        custom_data=['Total_str', 'Percentual']
    )
    

    # Ajustes de Rótulos e Tooltip
    fig.update_traces(
        # Rótulo externo: usa o %{percent} interno
        texttemplate="%{percent:.1%}",
        textposition="outside",
        
        # Tooltip: usa as variáveis internas %{label}, %{value} e %{percent}
        hovertemplate= (
            "<b>%{label}</b><br>"
            "Total: %{value:,.3f}K<br>" # Formata o valor com separador de milhar
            "Percentual: %{percent:.1%}" # Formata o percentual
            "<extra></extra>"
        ),
        sort=True
    )

    # Ajustes de Layout
    fig.update_layout(
        template=tema,
        margin=dict(t=25, l=0, r=0, b=0),
        font=dict(size=13),
        showlegend=True
        # 'coloraxis_showscale=False' removido, pois não há eixo de cor
    )

    # Renderiza
    return st.plotly_chart(fig, use_container_width=True)

# Grafico de area


def grafico_treemap(df, coluna_categoria, coluna_valor=None, titulo=None, top_n=None):
    
    if titulo:
        st.subheader(titulo)

    # Agregação dos dados
    if coluna_valor is None:
        total = df.groupby(coluna_categoria).size().reset_index(name='Total')
    else:
        total = df.groupby(coluna_categoria)[coluna_valor].sum().reset_index(name='Total')

    # 2. Limita Top N categorias
    if top_n is not None:
        total = total.nlargest(top_n, 'Total')

    # Ordena do maior para o menor
    total = total.sort_values('Total', ascending=False)

    # Calcula percentual
    total['Percentual'] = (total['Total'] / total['Total'].sum() * 100).round(1)

    # Cria coluna formatada com ponto de milhar
    total['Total_str'] = formatar_milhar(total['Total'])

    # Texto dentro do bloco: valor + percentual
    total['Texto'] = total['Total_str'] + " (" + total['Percentual'].astype(str) + "%)"

    # Criação do Treemap
    fig = px.treemap(
        total,
        path=[coluna_categoria],
        values='Total',
        color='Total',
        color_continuous_scale='Blues'
    )

    # Exibir o valor dentro do bloco e desativar tooltip
    fig.update_traces(
        texttemplate="%{label}<br>%{customdata[0]}",
        textinfo="label+text",
        customdata=total[['Texto']],
        hoverinfo='skip',     # remove completamente o hover
        hovertemplate=None
    )

    # Ajustes de layout
    fig.update_layout(
        margin=dict(t=25, l=0, r=0, b=0),
        font=dict(size=14),
        coloraxis_colorbar=dict(title="Total")
    )

    # Renderiza no Streamlit
    return st.plotly_chart(fig, use_container_width=True)


def grafico_linha(df, coluna_x, coluna_y=None, titulo=None, top_n=None, freq=None):
    

    if titulo:
        st.subheader(titulo)

    # Verifica se coluna_x existe
    if coluna_x not in df.columns:
        st.error(f"Erro: Coluna '{coluna_x}' não encontrada.")
        return

    # Detecta tipo de coluna
    is_date_column = pd.api.types.is_datetime64_any_dtype(df[coluna_x])
    if is_date_column:
        df[coluna_x] = pd.to_datetime(df[coluna_x])

    # Agrupamento
    if is_date_column:
        freq = freq or 'MS'  # padrão mês
        if coluna_y is None:
            total = df.groupby(pd.Grouper(key=coluna_x, freq=freq)).size().reset_index(name='Total')
        else:
            total = df.groupby(pd.Grouper(key=coluna_x, freq=freq))[coluna_y].sum().reset_index(name='Total')

        # Preenche todos os valores do eixo
        todas_datas = pd.date_range(start=total[coluna_x].min(),
                                    end=total[coluna_x].max(),
                                    freq=freq)
        total = pd.merge(pd.DataFrame({coluna_x: todas_datas}),
                         total,
                         on=coluna_x,
                         how='left')
        total['Total'] = total['Total'].fillna(0)
        total['Percentual'] = (total['Total'] / total['Total'].sum() * 100).round(1) if total['Total'].sum() else 0
        # Formatação Mês/Ano ou hora
        if freq in ['H', 'h']:
            total['Eixo'] = total[coluna_x].dt.strftime('%H:%M')
        else:
            total['Eixo'] = total[coluna_x].dt.strftime('%b/%Y')

    else:
        if coluna_y is None:
            total = df.groupby(coluna_x).size().reset_index(name='Total')
        else:
            total = df.groupby(coluna_x)[coluna_y].sum().reset_index(name='Total')
        total['Percentual'] = (total['Total'] / total['Total'].sum() * 100).round(1) if total['Total'].sum() else 0
        if top_n:
            total = total.nlargest(top_n, 'Total')
        total = total.sort_values(coluna_x)
        total['Eixo'] = total[coluna_x].astype(str)

    # Tema Plotly automático
    tema = 'plotly_white' if st.get_option("theme.base") == "light" else 'plotly_dark'
    total['Total_str'] = formatar_milhar(total['Total'])
    # Criação do gráfico
    fig = px.line(
        total,
        x='Eixo',
        y='Total',
        markers=True,
        text='Total_str',
        labels={'Total': 'Total', 'Eixo': coluna_x}
        #title=titulo
    )

    fig.update_traces(textposition='top center')

    # Ajustes do layout
    fig.update_layout(
        template=tema,
        hovermode='x unified',
        #title_x=0.5,
        xaxis_title=coluna_x,
        yaxis_title=None
    )

    # Força o eixo X como categórico para mostrar todos os itens
    fig.update_xaxes(type='category')

    st.plotly_chart(fig, use_container_width=True)

# Gráfico de radar

def grafico_radar(df, coluna_categoria, coluna_grupo, titulo):
    
    st.subheader(titulo)

    # Verifica se as colunas existem
    if coluna_categoria not in df.columns:
        st.error(f"Coluna '{coluna_categoria}' não encontrada no DataFrame.")
        return
    if coluna_grupo and coluna_grupo not in df.columns:
        st.error(f"Coluna '{coluna_grupo}' não encontrada no DataFrame.")
        return

    # Agrupa os dados (conta registros)
    if coluna_grupo:
        df_agg = df.groupby([coluna_categoria, coluna_grupo]).size().reset_index(name='Total')
    else:
        df_agg = df.groupby(coluna_categoria).size().reset_index(name='Total')

    # Calcula percentual sobre o total geral
    total_geral = df_agg['Total'].sum()
    df_agg['Percentual'] = (df_agg['Total'] / total_geral * 100).round(2)

    # Cria gráfico radar
    fig = px.line_polar(
        df_agg,
        r='Total',
        theta=coluna_categoria,
        color=coluna_grupo if coluna_grupo else None,
        line_close=True,
        hover_data={'Total': True, 'Percentual': True},
        template='plotly_white'
    )

    fig.update_traces(fill='toself', hovertemplate='%{theta}<br>Total: %{r}<br>%{customdata[1]}%<extra></extra>')
    fig.update_layout(
        #title=titulo,
        polar=dict(radialaxis=dict(visible=True, linewidth=1, gridcolor='lightgray')),
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)
    

def grafico_scater(df, coluna_x, coluna_y, tamanho_y, cor_bola, nome_bola, titulo, key=None):
    
    st.subheader(titulo)

    #  Gera o gráfico 
    fig = px.scatter(
        df,
        x=coluna_x,
        y=coluna_y,
        size=tamanho_y,
        color=cor_bola,
        hover_name=nome_bola   # mostra apenas o nome da bola no tooltip
        #title=titulo
    )
    fig.update_layout(height=500)

    #  Define uma chave única se não fornecida ---
    if key is None:
        key = f"{coluna_x}_{coluna_y}_{cor_bola}"

    return st.plotly_chart(fig, use_container_width=True, key=key)




# Grafico de mapas de calor

def grafico_heatmap(df, coluna_valor, titulo):
    
    st.subheader(titulo)
    
    if df is None or df.empty:
        return None

    colunas_necessarias = {'Latitude', 'Longitude', coluna_valor}
    if not colunas_necessarias.issubset(df.columns):
        return None

    # Limpeza e conversões 
    df = df.dropna(subset=['Latitude', 'Longitude', coluna_valor]).copy()
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
    df[coluna_valor] = pd.to_numeric(df[coluna_valor], errors='coerce')
    df['Km'] = pd.to_numeric(df.get('Km', 0), errors='coerce')
    df = df.dropna(subset=['Latitude', 'Longitude', coluna_valor])

    if df.empty:
        return None

    #  Ajuste de escala e saturação 
    valor_95 = np.percentile(df[coluna_valor], 95)
    range_color = [0, valor_95]

    if coluna_valor == "Mortos":
        escala = "Reds"
    elif coluna_valor == "Feridos":
        escala = "Purples"
    else:
        escala = "Blues"

    #  Ajuste dinâmico de raio e zoom 
    n_pontos = len(df)
    if n_pontos > 15000:
        raio_mapa = 6
        zoom = 3.5
    elif n_pontos > 5000:
        raio_mapa = 8
        zoom = 4
    elif n_pontos > 1000:
        raio_mapa = 12
        zoom = 4.3
    else:
        raio_mapa = 16
        zoom = 4.8  #  mais próximo e detalhado

    #  Geração do mapa 
    fig = px.density_mapbox(
        df,
        lat='Latitude',
        lon='Longitude',
        z=coluna_valor,
        radius=raio_mapa,
        hover_data={
            'Região': True if 'Região' in df.columns else False,
            'Uf': True if 'Uf' in df.columns else False,
            'Municipio': True if 'Municipio' in df.columns else False,
            'Br': True if 'Br' in df.columns else False,
            'Km': ':.1f' if 'Km' in df.columns else False,
            coluna_valor: ':.0f'
        },
        center=dict(lat=-14.2, lon=-54.0),  # foco no centro do Brasil
        zoom=zoom,
        mapbox_style="carto-positron",  # mais leve e compatível
        color_continuous_scale=escala,
        range_color=range_color,
        #title=titulo
    )

    #  Aparência geral 
    fig.update_layout(
        height=650,
        margin=dict(l=0, r=0, t=60, b=0),
        coloraxis_colorbar=dict(
            title=coluna_valor,
            thicknessmode="pixels",
            thickness=18,
            lenmode="fraction",
            len=0.7,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    # Contraste e opacidade para nitidez
    fig.update_traces(opacity=0.85)

    return fig






    
    
def grafico_coluna(df, coluna_x, coluna_y=None, titulo=None, top_n=None):
    
    # Subtítulo no Streamlit
    if titulo:
        st.subheader(titulo)

    # Preparação dos dados
    if coluna_y is None:
        total = df.groupby(coluna_x).size().reset_index(name='Total')
    else:
        total = df.groupby(coluna_x)[coluna_y].sum().reset_index(name='Total')

    # Limita categorias
    if top_n is not None:
        total = total.nlargest(top_n, 'Total')

    # Ordena para exibir colunas em ordem decrescente
    total = total.sort_values('Total', ascending=True)

    # Força eixo categórico a ser string
    total[coluna_x] = total[coluna_x].astype(str)

    # Formata valor e percentual
    soma_total = total['Total'].sum()
    total['Total_str'] = total['Total'].apply(formatar_milhar)
    total['Percentual'] = (total['Total'] / soma_total * 100).round(1) if soma_total else 0

    # Tema automático
    tema = 'plotly_white' if st.get_option("theme.base") == "light" else 'plotly_dark'

    # Criação do gráfico
    fig = px.bar(
        total,
        x='Total',
        y=coluna_x,
        text='Total_str',
        hover_data={'Percentual': True},
    )

    fig.update_traces(
        marker_color='#1f77b4',  # cor fixa aqui
        textposition='outside'
    )
    

    fig.update_layout(
        template=tema,
        yaxis=dict(title=None, showticklabels=True),
        xaxis=dict(title=None, showticklabels=True, categoryorder='total descending'),
        showlegend=False,
        margin=dict(t=25, l=0, r=0, b=0),
        font=dict(size=13),
    )

    st.plotly_chart(fig, use_container_width=True)