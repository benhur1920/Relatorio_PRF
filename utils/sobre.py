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
                    A análise de dados de acidentes de trânsito é essencial para compreender a dinâmica da segurança viária no 
                    Brasil e subsidiar ações preventivas mais eficazes.
                </p>
                <p>
                    Este aplicativo foi desenvolvido com base em dados públicos da Polícia Rodoviária Federal (PRF), que 
                    registram as ocorrências de acidentes nas rodovias federais de todo o país.
                </p>
                <p>
                    Os números são alarmantes. Vivemos uma verdadeira situação de guerra, com a perda de inúmeras vidas e um 
                    elevado número de feridos, o que gera grandes impactos sociais e econômicos. Além do sofrimento das famílias,
                      há prejuízos significativos para as empresas e vultosos gastos públicos com saúde e recuperação de 
                      infraestrutura.
                </p>
                <p>
                    O objetivo deste trabalho é transformar esses dados em informações úteis, possibilitando a identificação de 
                    padrões e tendências sobre os acidentes — como locais, horários, tipos de ocorrência, veículos envolvidos e 
                    vítimas.
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
