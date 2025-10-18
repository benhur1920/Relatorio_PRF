import streamlit as st
import altair as alt
import plotly.express as px

def grafico_barra(df, coluna_x, coluna_y=None, titulo=None, top_n=None):
    """
    Cria gráfico Altair dinâmico, com texto sobre as barras.
    - coluna_x: eixo X (Ano, Mês, Região, etc.)
    - coluna_y: soma de valores (Mortos, Feridos, Veiculos) ou None para contar linhas
    - top_n: para limitar categorias
    - titulo: título do gráfico
    """
    if titulo:
        st.subheader(titulo)

    if coluna_y is None:
        total = df.groupby(coluna_x).size().reset_index(name='Total')
    else:
        total = df.groupby(coluna_x)[coluna_y].sum().reset_index(name='Total')

    # Top N para categorias
    if top_n is not None:
        total = total.nlargest(top_n, 'Total')

    # Ordena do maior para o menor
    total = total.sort_values('Total', ascending=False)

    bar = alt.Chart(total).mark_bar().encode(
    x=alt.X(coluna_x, type='nominal', sort=alt.EncodingSortField(field="Total", order="descending")),
    y='Total:Q',
    tooltip=[coluna_x, 'Total']
)

    text = bar.mark_text(
        align='center',
        baseline='bottom',
        dy=-5
    ).encode(
        text='Total:Q'
    )

    chart = alt.layer(bar, text)
    fig = st.altair_chart(chart, use_container_width=True)
    return fig

def grafico_coluna(df, coluna_x, coluna_y=None, titulo=None, top_n=None):
    """
    Cria gráfico Altair de BARRAS HORIZONTAIS, com texto sobre as barras.
    - coluna_x: eixo Y (Categoria: Ano, Mês, Região, etc.)
    - coluna_y: soma de valores (Eixo X: Mortos, Feridos, etc.) ou None para contar linhas
    - top_n: para limitar categorias
    - titulo: título do gráfico
    """
    if titulo:
        st.subheader(titulo)

    # --- Nenhuma mudança na preparação dos dados ---
    if coluna_y is None:
        total = df.groupby(coluna_x).size().reset_index(name='Total')
    else:
        total = df.groupby(coluna_x)[coluna_y].sum().reset_index(name='Total')

    if top_n is not None:
        total = total.nlargest(top_n, 'Total')

    # A ordenação aqui é importante para o eixo Y
    # Note que a ordem no 'sort' do eixo Y será 'descending'
    total = total.sort_values('Total', ascending=True)

    # --- Mudanças no Gráfico ---

    # Invertemos X e Y
    bar = alt.Chart(total).mark_bar().encode(
        # X agora é o valor quantitativo
        x=alt.X('Total:Q'), 
        # Y agora é a categoria nominal
        y=alt.Y(coluna_x, type='nominal', 
                # Ordena as categorias pelo Total, do maior (topo) para o menor (baixo)
                sort=alt.EncodingSortField(field="Total", order="descending")),
        tooltip=[coluna_x, 'Total']
    )

    # Ajustamos a posição do texto
    text = bar.mark_text(
        align='left',     # Alinha o texto à esquerda (fora da barra)
        baseline='middle',
        dx=5              # Desloca o texto 5 pixels para a DIREITA (eixo x)
    ).encode(
        text='Total:Q'
    )

    chart = alt.layer(bar, text)
    fig = st.altair_chart(chart, use_container_width=True)
    return fig

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

    # 1. Mesma lógica de agregação da sua função original
    if coluna_valor is None:
        # Conta as ocorrências (linhas)
        total = df.groupby(coluna_categoria).size().reset_index(name='Total')
    else:
        # Soma a coluna especificada
        total = df.groupby(coluna_categoria)[coluna_valor].sum().reset_index(name='Total')

    # 2. Top N para categorias
    if top_n is not None:
        total = total.nlargest(top_n, 'Total')

    # 3. Cálculo de Percentual (Essencial para pizza)
    total['percent'] = total['Total'] / total['Total'].sum()

    # Ordena do maior para o menor (bom para a legenda e ordem da pizza)
    total = total.sort_values('Total', ascending=False)

    # --- Criação do Gráfico de Pizza ---

    # Gráfico base
    base = alt.Chart(total).encode(
       theta=alt.Theta("Total:Q", stack=True)
    )

    # As fatias da pizza
    # outerRadius define o tamanho da pizza
    pie = base.mark_arc(outerRadius=120).encode(
        # A cor será baseada na categoria
        color=alt.Color(f"{coluna_categoria}:N"),
        # Ordena as fatias do maior para o menor
        order=alt.Order("percent", sort="descending"),
        # Tooltip ao passar o mouse
        tooltip=[coluna_categoria, 
                 "Total", 
                 alt.Tooltip("percent", format=".1%")]
    )

    # O texto (rótulos de percentual)
    text = base.mark_text(radius=140).encode(
        # Mostra o percentual formatado
        text=alt.Text("percent", format=".1%"),
        # Ordena os rótulos igual às fatias
        order=alt.Order("percent", sort="descending"),
        # Define a cor do texto para preto
        color=alt.value("black")  
    )

    # Combina as fatias e os rótulos
    chart = alt.layer(pie, text)

    fig = st.altair_chart(chart, use_container_width=True)
    return fig






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

    # 1. Lógica de agregação (sem alteração)
    if coluna_valor is None:
        total = df.groupby(coluna_categoria).size().reset_index(name='Total')
    else:
        total = df.groupby(coluna_categoria)[coluna_valor].sum().reset_index(name='Total')

    # 2. Top N (sem alteração)
    if top_n is not None:
        total = total.nlargest(top_n, 'Total')

    # 3. Ordenação (sem alteração)
    total = total.sort_values('Total', ascending=False)
    
    # 4. Criação do Gráfico Treemap (COM AS MUDANÇAS)
    fig = px.treemap(
        data_frame=total,
        path=[coluna_categoria], 
        values='Total',
        
        # --- MUDANÇAS AQUI ---
        color='Total', # 1. Cor baseada no valor numérico 'Total'
        color_continuous_scale='Blues', # 2. Usar a escala de cores 'Blues'
        # --- FIM DAS MUDANÇAS ---
        
        hover_name=coluna_categoria,
        hover_data={'Total': ':.0f'} 
    )

    # 5. Ajustes de layout (sem alteração)
    fig.update_layout(
        margin=dict(t=25, l=0, r=0, b=0),
        font=dict(size=14)
    )
    
    # Esta linha agora controla a barra de gradiente
    fig.update_layout(coloraxis_colorbar=dict(
        title="Total"
    ))

    # 6. Renderiza no Streamlit (sem alteração)
    fig_st = st.plotly_chart(fig, use_container_width=True)
    return fig_st

