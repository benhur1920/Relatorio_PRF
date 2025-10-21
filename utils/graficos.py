import streamlit as st
import altair as alt
import plotly.express as px
import pandas as pd

def grafico_barra(df, coluna_x, coluna_y=None, titulo=None, top_n=None):
    """
    Cria gráfico Altair dinâmico, com texto sobre as barras e percentual no tooltip.
    - coluna_x: eixo X (Ano, Mês, Região, etc.)
    - coluna_y: soma de valores (Mortos, Feridos, Veiculos) ou None para contar linhas
    - top_n: para limitar categorias
    - titulo: título do gráfico
    """
    if titulo:
        st.subheader(titulo)

    # Preparação dos dados
    if coluna_y is None:
        total = df.groupby(coluna_x).size().reset_index(name='Total')
    else:
        total = df.groupby(coluna_x)[coluna_y].sum().reset_index(name='Total')

    if top_n is not None:
        total = total.nlargest(top_n, 'Total')

    total = total.sort_values('Total', ascending=False)

    # Calcula percentual
    soma_total = total['Total'].sum() if len(total) > 0 else 0
    total['Percentual'] = (total['Total'] / soma_total * 100).round(1) if soma_total else 0

    # Gráfico de barras com cor fixa e tooltip com percentual
    bar = alt.Chart(total).mark_bar(color='#1f77b4').encode(
        x=alt.X(coluna_x, type='nominal',
                sort=alt.EncodingSortField(field="Total", order="descending")),
        y=alt.Y('Total:Q'),
        tooltip=[
            alt.Tooltip(coluna_x, title='Categoria'),
            alt.Tooltip('Total:Q', title='Total', format=','),
            alt.Tooltip('Percentual:Q', title='Percentual (%)', format='.1f')
        ]
    )

    # Texto acima das barras mostrando apenas o total
    text = bar.mark_text(
        align='center',
        baseline='bottom',
        dy=-5,
        color='black'
    ).encode(
        text=alt.Text('Total:Q', format=',')
    )

    chart = alt.layer(bar, text).properties(width='container')
    return st.altair_chart(chart, use_container_width=True)

def grafico_barra_sem_ordenar(df, coluna_x, coluna_y=None, titulo=None, top_n=None):
    """
    Cria gráfico Altair dinâmico, com texto sobre as barras e percentual no tooltip.
    - coluna_x: eixo X (Ano, Mês, Região, etc.)
    - coluna_y: soma de valores (Mortos, Feridos, Veiculos) ou None para contar linhas
    - top_n: para limitar categorias
    - titulo: título do gráfico
    """
    if titulo:
        st.subheader(titulo)

    # Preparação dos dados
    if coluna_y is None:
        total = df.groupby(coluna_x).size().reset_index(name='Total')
    else:
        total = df.groupby(coluna_x)[coluna_y].sum().reset_index(name='Total')

    if top_n is not None:
        total = total.nlargest(top_n, 'Total')

    

    # Calcula percentual
    soma_total = total['Total'].sum() if len(total) > 0 else 0
    total['Percentual'] = (total['Total'] / soma_total * 100).round(1) if soma_total else 0
    
   # Gráfico de barras com cor fixa e tooltip com percentual
    bar = alt.Chart(total).mark_bar(color='#1f77b4').encode(
        x=alt.X(coluna_x, type='nominal'),
        y=alt.Y('Total:Q'),
        tooltip=[
            alt.Tooltip(coluna_x, title='Categoria'),
            alt.Tooltip('Total:Q', title='Total', format=','),
            alt.Tooltip('Percentual:Q', title='Percentual (%)', format='.1f')
        ]
    )

    # Texto acima das barras mostrando apenas o total
    text = bar.mark_text(
        align='center',
        baseline='bottom',
        dy=-5,
        color='black'
    ).encode(
        text=alt.Text('Total:Q', format=',')
    )

    chart = alt.layer(bar, text).properties(width='container')
    return st.altair_chart(chart, use_container_width=True)



def grafico_coluna(df, coluna_x, coluna_y=None, titulo=None, top_n=None):
    """
    Cria gráfico Altair de BARRAS HORIZONTAIS simples.
    - coluna_x: eixo Y (Categoria: Ano, Mês, Região, etc.)
    - coluna_y: soma de valores (Eixo X: Mortos, Feridos, etc.) ou None para contar linhas
    - top_n: limita número de categorias exibidas
    - titulo: título opcional do gráfico
    """
    if titulo:
        st.subheader(titulo)

    # --- Prepara dados ---
    if coluna_y is None:
        total = df.groupby(coluna_x).size().reset_index(name='Total')
    else:
        total = df.groupby(coluna_x)[coluna_y].sum().reset_index(name='Total')

    if top_n is not None:
        total = total.nlargest(top_n, 'Total')

    total = total.sort_values('Total', ascending=True)
    total['Percentual'] = (total['Total'] / total['Total'].sum() * 100).round(1)

    # --- Tema geral ---
    alt.themes.enable('none')
    alt.data_transformers.disable_max_rows()

    # --- Gráfico principal ---
    bar = alt.Chart(total).mark_bar(color='#1f77b4').encode(
        x=alt.X('Total:Q',
                title='',
                axis=alt.Axis(labels=False, ticks=False, domain=False)
        ),
        y=alt.Y(coluna_x,
                sort=alt.EncodingSortField(field="Total", order="descending"),
                title='',
                axis=alt.Axis(labelFontSize=12, labelLimit=250)
        ),
        tooltip=[
            alt.Tooltip(coluna_x, title='Categoria'),
            alt.Tooltip('Total:Q', title='Total', format=','),
            alt.Tooltip('Percentual:Q', title='Percentual (%)', format='.1f')
        ]
    )

    # --- Texto sobre as barras ---
    text = bar.mark_text(
        align='left',
        baseline='middle',
        dx=6,
        fontSize=12,
        color='black'
    ).encode(
        text=alt.Text('Total:Q', format=',')
    )

    # --- Junta gráfico e texto ---
    chart = (bar + text).properties(
        width='container',
        height=max(300, len(total) * 25)
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        grid=False
    )

    return st.altair_chart(chart, use_container_width=True)

def grafico_pizza(df, coluna_categoria, coluna_valor=None, titulo=None, top_n=None):
    """
    Cria gráfico de Pizza (torta) Altair dinâmico, com rótulos de percentual.
    - coluna_categoria: A fatia da pizza (Região, Tipo Acidente, etc.)
    - coluna_valor: soma de valores (Mortos, Feridos) ou None para contar linhas
    - top_n: para limitar categorias
    - titulo: título do gráfico
    """
    if titulo:
        st.subheader(titulo)

    # 1. Agregação dos dados
    if coluna_valor is None:
        total = df.groupby(coluna_categoria).size().reset_index(name='Total')
    else:
        total = df.groupby(coluna_categoria)[coluna_valor].sum().reset_index(name='Total')

    # 2. Limita as categorias
    if top_n is not None:
        total = total.nlargest(top_n, 'Total')

    # 3. Calcula percentual
    total['percent'] = total['Total'] / total['Total'].sum()

    # Ordena do maior para o menor
    total = total.sort_values('Total', ascending=False)

    # --- Gráfico de Pizza ---
    base = alt.Chart(total).encode(
        theta=alt.Theta("Total:Q", stack=True),
        order=alt.Order("percent", sort="descending")
    )

    # Fatias com tons de azul e tooltip
    pie = base.mark_arc(outerRadius=120).encode(
        color=alt.Color(f"{coluna_categoria}:N",
                        scale=alt.Scale(scheme='blues')),
        tooltip=[
            alt.Tooltip(coluna_categoria, title='Categoria'),
            alt.Tooltip('Total:Q', title='Total', format=','),
            alt.Tooltip('percent:Q', title='Percentual', format='.1%')
        ]
    )

    # Rótulos com percentual fora da pizza
    text = base.mark_text(radius=140, font='Arial', fontSize=12, color='black').encode(
        text=alt.Text("percent", format=".1%")
    )

    # Combina e mostra
    chart = alt.layer(pie, text).properties(
        width=400,
        height=400
    ).configure_view(
        strokeWidth=0
    )

    return st.altair_chart(chart, use_container_width=True)





def grafico_treemap(df, coluna_categoria, coluna_valor=None, titulo=None, top_n=None):
    """
    Cria gráfico Treemap interativo com Plotly Express em TONS DE AZUL.
    - coluna_categoria: As caixas do treemap (Região, Tipo Acidente, etc.)
    - coluna_valor: O tamanho das caixas (Mortos, Feridos) ou None para contar linhas
    - top_n: para limitar categorias
    - titulo: título do gráfico
    """
    if titulo:
        st.subheader(titulo)

    # 1. Agregação dos dados
    if coluna_valor is None:
        total = df.groupby(coluna_categoria).size().reset_index(name='Total')
    else:
        total = df.groupby(coluna_categoria)[coluna_valor].sum().reset_index(name='Total')

    # 2. Limita Top N categorias
    if top_n is not None:
        total = total.nlargest(top_n, 'Total')

    # 3. Ordena do maior para o menor
    total = total.sort_values('Total', ascending=False)

    # 4. Calcula percentual
    total['Percentual'] = (total['Total'] / total['Total'].sum() * 100).round(1)

    # 5. Criação do Treemap
    fig = px.treemap(
        total,
        path=[coluna_categoria],
        values='Total',
        color='Total',
        color_continuous_scale='Blues',  # tons de azul
        hover_name=coluna_categoria,
        hover_data={
            'Total': ':.0f',
            'Percentual': ':.1f'  # mostra percentual no tooltip
        }
    )

    # 6. Ajustes de layout
    fig.update_layout(
        margin=dict(t=25, l=0, r=0, b=0),
        font=dict(size=14),
        coloraxis_colorbar=dict(title="Total")
    )

    # 7. Renderiza no Streamlit
    return st.plotly_chart(fig, use_container_width=True)

def grafico_linha(df, coluna_x, coluna_y=None, titulo=None, top_n=None):
    """
    Cria gráfico de linha Altair dinâmico.
    - Se coluna_x for data, agrupa por Mês/Ano.
    - Se coluna_x for categoria, agrupa por categoria.
    - Tooltip habilitado, SEM rótulos nos pontos.
    """
    if titulo:
        st.subheader(titulo)

    # 1. Verifica se a coluna_x é do tipo datetime
    try:
        is_date_column = pd.api.types.is_datetime64_any_dtype(df[coluna_x])
    except KeyError:
        st.error(f"Erro: Coluna '{coluna_x}' não encontrada.")
        return

    # 2. Agrupa os dados
    if is_date_column:
        # --- SE FOR DATA: Agrupa por Mês (MS = Month Start) ---
        grouper_mes = pd.Grouper(key=coluna_x, freq='MS')
        if coluna_y is None:
            total = df.groupby(grouper_mes).size().reset_index(name='Total')
        else:
            total = df.groupby(grouper_mes)[coluna_y].sum().reset_index(name='Total')
    else:
        # --- SE FOR CATEGORIA: Mantém a lógica original ---
        if coluna_y is None:
            total = df.groupby(coluna_x).size().reset_index(name='Total')
        else:
            total = df.groupby(coluna_x)[coluna_y].sum().reset_index(name='Total')

    # Limite de categorias (NÃO aplicar para datas, senão quebra a linha do tempo)
    if top_n is not None and not is_date_column:
        total = total.nlargest(top_n, 'Total')

    # Ordena pelo eixo X (funciona para datas e categorias)
    total = total.sort_values(by=coluna_x)

    # Calcula percentual
    soma_total = total['Total'].sum() if len(total) > 0 else 0
    total['Percentual'] = (total['Total'] / soma_total * 100).round(1) if soma_total else 0

    # 3. Define a formatação do Eixo X e Tooltip
    if is_date_column:
        # Formatação para datas (ex: Jan/2025)
        x_axis = alt.X(coluna_x, 
                       type='temporal', 
                       title='Mês/Ano',
                       axis=alt.Axis(format="%b/%Y"))
        tooltip_x = alt.Tooltip(coluna_x, title='Mês/Ano', format="%b/%Y")
    else:
        # Formatação para categorias (como estava antes)
        x_axis = alt.X(coluna_x, type='nominal', sort=None, title=coluna_x)
        tooltip_x = alt.Tooltip(coluna_x, title='Categoria')

    # 4. Gráfico de linha (o tooltip está definido aqui)
    line = alt.Chart(total).mark_line(point=True, color='#1f77b4').encode(
        x=x_axis,
        y=alt.Y('Total:Q', title='Total'),
        tooltip=[
            tooltip_x,
            alt.Tooltip('Total:Q', title='Total', format=','),
            alt.Tooltip('Percentual:Q', title='Percentual (%)', format='.1f')
        ]
    )

    # O gráfico agora é apenas a camada 'line'
    chart = line
    
    return st.altair_chart(chart, use_container_width=True)


def grafico_mapa_fatais(df):
    # 1. Definir colunas necessárias
    colunas_necessarias = [
        'Latitude', 'Longitude', 'Br', 'Municipio', 'Km',
        'Classificacao Acidente', 'Tipo Acidente', 'Mortos', 'Feridos'
    ]
    
    # 2. Verificar colunas
    colunas_faltando = [col for col in colunas_necessarias if col not in df.columns]
    if colunas_faltando:
        st.warning(f"Mapa Fatais: Colunas faltando: {', '.join(colunas_faltando)}")
        return None

    # --- MUDANÇA PRINCIPAL 1: Filtrar APENAS por Vítimas Fatais ---
    df_fatais = df[df['Classificacao Acidente'] == 'Com Vítimas Fatais'].copy()

    # 3. Verificar se há dados APÓS o filtro
    if df_fatais.empty:
        st.warning("Não há dados de acidentes fatais para os filtros selecionados.")
        return None

    # 4. Limpar Nulos de coordenadas
    df_mapa = df_fatais.dropna(subset=['Latitude', 'Longitude'])
    if df_mapa.empty:
        st.warning("Dados de acidentes fatais não possuem coordenadas válidas.")
        return None

    # 5. Criar o gráfico
    st.subheader("Mapa de Ocorrências Fatais")
    st.write("Cada ponto representa um acidente fatal, colorido pelo tipo.")
    
    fig = px.scatter_mapbox(
        df_mapa,
        lat='Latitude',
        lon='Longitude',
        
        # --- MUDANÇA PRINCIPAL 2: Colorir por Tipo de Acidente ---
        color='Tipo Acidente', 
        
        hover_name='Tipo Acidente',
        hover_data={
            'Br': True,
            'Km': True,
            'Municipio': True,
            'Mortos': True,
            'Feridos': True,
            'Latitude': False,
            'Longitude': False,
        },
        zoom=3.5,
        height=700
    )

    fig.update_traces(marker=dict(size=10))
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_center={"lat": -14.2350, "lon": -51.9253},
        legend=dict(
            title_text='Tipo de Acidente Fatal',
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5
        ),
        margin=dict(t=50, b=20, l=10, r=10)
    )
    return fig



def grafico_heatmap_fatais(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    
    must = ['latitude', 'longitude', 'classificacao acidente', 'mortos']
    faltando = [c for c in must if c not in df.columns]
    if faltando:
        st.warning(f"Mapa de Calor: Colunas faltando: {', '.join(faltando)}")
        return None
    
    df_fatais = df[df['classificacao acidente'].str.lower() == 'mortos'].copy()
    if df_fatais.empty:
        return None
    
    df_fatais['mortos'] = pd.to_numeric(df_fatais['mortos'], errors='coerce')
    df_mapa = df_fatais.dropna(subset=['latitude','longitude','mortos'])
    
    # Limites aproximados para o Brasil
    df_mapa = df_mapa[(df_mapa['latitude'].between(-33,5)) & (df_mapa['longitude'].between(-75,-32))]
    if df_mapa.empty:
        return None

    fig = px.density_mapbox(
        df_mapa, lat='latitude', lon='longitude', z='mortos',
        radius=12, center=dict(lat=-14.2350, lon=-51.9253), zoom=3.8,
        mapbox_style='carto-darkmatter',
        hover_name=None,
        hover_data={
            'causa acidente': True,
            'tipo acidente': True,
            'mortos': True
        },
        height=650,
        color_continuous_scale='Blues'
    )
    fig.update_layout(margin=dict(t=40,b=10,l=10,r=10), coloraxis_colorbar=dict(title='Mortos'))
    return fig


def grafico_radar(df, coluna_categoria, coluna_grupo, titulo):
    """
    Cria gráfico de radar (teia) interativo com Plotly.
    - coluna_categoria: eixo angular (ex: 'Grupo Via', 'Condicao Metereologica')
    - coluna_grupo: separação por cor (ex: 'Tipo Acidente')
    - titulo: título do gráfico
    """

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
        title=titulo,
        polar=dict(radialaxis=dict(visible=True, linewidth=1, gridcolor='lightgray')),
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)



def grafico_heatmap(df, coluna_valor, titulo):
    """
    Cria um mapa de calor dinâmico (Mortes, Feridos ou Acidentes).
    Mostra no tooltip: Região, UF, Município, BR e KM.
    """
    if df is None or df.empty:
        return None

    colunas_necessarias = {'Latitude', 'Longitude', coluna_valor}
    if not colunas_necessarias.issubset(df.columns):
        return None

    df = df.dropna(subset=['Latitude', 'Longitude', coluna_valor])
    if df.empty:
        return None

    # Converte colunas numéricas
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
    df[coluna_valor] = pd.to_numeric(df[coluna_valor], errors='coerce')
    df['Km'] = pd.to_numeric(df.get('Km', 0), errors='coerce')

    # Escolhe escala de cores conforme o tipo
    if coluna_valor == "Mortos":
        escala = "Reds"
    elif coluna_valor == "Feridos":
        escala = "greys"
    else:
        escala = "Blues"

    # Cria o mapa de calor
    fig = px.density_mapbox(
        df,
        lat='Latitude',
        lon='Longitude',
        z=coluna_valor,
        radius=5,  # menor raio = mais leve e mais rápido
        hover_data={
            'Região': True,
            'Uf': True,
            'Municipio': True,
            'Br': True,
            'Km': ':.1f',
            coluna_valor: True
        },
        center=dict(lat=-15.78, lon=-52.0),  # centro mais aberto
        zoom=3,
        mapbox_style='carto-positron',
        color_continuous_scale=escala,
        title=titulo
    )

    fig.update_layout(height=600, margin=dict(l=0, r=0, t=50, b=0))
    return fig