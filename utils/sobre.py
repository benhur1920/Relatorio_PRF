import streamlit as st
import os
#from utils.totalizadores import *
from utils.marcadores import divisor

def sobre():
    
      
    
    imagem_path1 = os.path.join("imagem", "estrada.jpg")

    st.markdown("<h2 style='text-align: center; '>🚨 Introdução ao Estudo dos Acidentes Rodoviários da PRF</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Primeira seção com imagem e texto
    col1, col2 = st.columns([2, 3], gap="small")

    with col1:
        st.image(imagem_path1, use_container_width=True, caption="Trecho de uma estrada")


    with col2:
        
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


def objetivo_aplicacao():
    imagem_path2 = os.path.join(os.path.dirname(__file__), '..', 'images', 'lampada.jpg')
    col1, col2 = st.columns([3, 2], gap="small")
    with col1:
        st.markdown("""
        <div contenteditable="false" style="text-align: justify; font-size: 17px;">
            <h3>PredictImóvel Recife</h3>
            <p>
                Esta ferramenta permitirá  estimar o valor venal com base em estudos estatísticos da base de dados
                do ITBI da Prefeitura do Recife.
            </p>
            <p>Os principais enfoques são:</p>
            <ul>
                <li><strong>Distribuição entre zonas e bairros da cidade</strong></li>
                <li><strong>Cálculo de medidas de tendência central e dispersão</strong></li>
                <li><strong>Consulta e exploração da base de dados</strong></li>
                <li><strong>Estimativa preditiva do valor venal utilizando técnicas de Machine Learning</strong></li>
            </ul>
            <p>
                Navegue entre as páginas e conheça os painéis das transmissões imobiliárias na cidade do Recife.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.image(imagem_path2, use_container_width=True, clamp=True, caption="Boa ideia")

def mainSobre():
    divisor()
    sobre()
    divisor()
    #objetivo_aplicacao()
    #divisor()
