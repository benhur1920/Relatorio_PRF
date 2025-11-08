import streamlit as st
import os
from utils.marcadores import divisor

def sobre():
    # Imagens do app
    imagem_path1 = os.path.join("imagem", "estrada.jpg")
    imagem_path2 = os.path.join("imagem", "silhueta-de-familia-feliz-na-sunset.jpg")
    imagem_path3 = os.path.join("imagem", "estrada-sinuosa-com-cerca-de-madeira-em-uma-floresta-de-montanha-floresta-verde-clara-contra-o-ceu-azul.jpg")

    # Título da página Sobre
    st.markdown("<h2 style='text-align: center; '>🚨 Introdução ao Estudo dos Acidentes Rodoviários da PRF</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Primeira seção com imagem e texto
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.image(imagem_path1, use_container_width=True, caption="Tempo bom para viagem")
    with col2:    
        st.image(imagem_path2, use_container_width=True, caption="Família")

    with col3:
        st.image(imagem_path3, use_container_width=True, caption="Trecho de estrada - Curvas")

    st.markdown(
            """
            <div style="text-align: justify; font-size: 17px">
                <p>
                    A análise dos dados de acidentes de trânsito é fundamental para compreender a dinâmica da segurança viária 
                    no Brasil e orientar políticas públicas mais eficazes de prevenção. De acordo com a Polícia Rodoviária 
                    Federal (PRF), a malha rodoviária brasileira soma aproximadamente 74 mil quilômetros, em um país de 
                    dimensões continentais, com trechos de pista simples, dupla e múltipla, variando entre bons e precários 
                    estados de conservação.
                </p>
                <p>
                    Neste estudo, utilizamos a base de dados da PRF, proveniente dos relatórios de ocorrências que registram 
                    sinistros nas rodovias federais de todo o país. A partir dessas informações, analisamos aspectos como 
                    tipo de rodovia, causa dos acidentes e condições meteorológicas, entre outros fatores determinantes.
                </p>
                <p>
                    Os números revelam uma realidade preocupante: vivemos uma verdadeira situação de guerra no trânsito, com 
                    a perda de inúmeras vidas e um elevado número de feridos — gerando impactos sociais e econômicos expressivos. 
                    Além do sofrimento humano, há prejuízos significativos para empresas e altos custos públicos com saúde, 
                    previdência e recuperação de infraestrutura.
                </p>
                <p>
                    O objetivo deste estudo é dar vida aos dados — transformar números em informação clara e visual, ajudando a 
                    identificar padrões, horários críticos, locais de maior risco e tipos de ocorrência. Com isso, queremos 
                    estimular a reflexão e contribuir para um trânsito mais seguro, mostrando que cada dado carrega uma 
                    história e pode inspirar uma mudança.
                </p>
            </div>
            """,
        unsafe_allow_html=True
    )


def mainSobre():
    divisor()
    sobre()
    divisor()
    
