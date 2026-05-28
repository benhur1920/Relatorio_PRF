import pandas as pd
import os
from pathlib import Path

BASE_DIR = Path(r'C:\Users\Ben-Hur\Desktop\PRF copia com codigos antigos\dados')
ANOS = range(2021, 2027)

def carregar_e_concatenar(anos, pasta):
    lista_dfs = []
    
    for ano in anos:
        caminho = os.path.join(pasta, f'datatran{ano}.csv')
        
        if not os.path.exists(caminho):
            print(f'Arquivo não encontrado: {caminho}')
            continue
        
        df = pd.read_csv(
            caminho,
            sep=None,
            engine='python',
            encoding='latin1',
            on_bad_lines='skip'
        )
        
        df['ano'] = ano
        lista_dfs.append(df)
    
    if not lista_dfs:
        raise ValueError("Nenhum arquivo foi carregado.")
    
    return pd.concat(lista_dfs, ignore_index=True)

def ajustar_coluna_data_inversa(df):
    df['data_inversa'] = pd.to_datetime(df['data_inversa'])
    return df

def gerar_colunas_derivadas_como_inteiros(df):
    df = df.drop(columns=['ano'])
    df['Ano'] = df['data_inversa'].dt.year.astype('Int64')
    df['Mês'] = df['data_inversa'].dt.month.astype('Int64')
    df['Dia'] = df['data_inversa'].dt.day.astype('Int64')
    return df

def criar_mapa_meses(df):
    mapa_meses = {
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro'
}

    # 2. Aplique o .map() à sua coluna 'mes'
    # (Assumindo que seu DataFrame se chama 'df')
    df['Mês'] = df['Mês'].map(mapa_meses)
    return df

def alterar_nome_coluna_data_inversa(df):
    df.rename(columns={'data_inversa': 'data'}, inplace=True)
    return df


def criar_coluna_partes_dia(df):
    # Converter a coluna 'horario' para datetime (somente hora)
    horas = pd.to_datetime(df['horario'], format='%H:%M:%S', errors='coerce').dt.hour

    # Criar nova coluna 'partes_dia' conforme as faixas
    df['Partes_dia'] = pd.cut(
        horas,
        bins=[-1, 5, 11, 17, 23],
        labels=['Madrugada', 'Manhã', 'Tarde', 'Noite']
    )

    return df


def converter_coluna_horario_para_datatime(df):
    # 1. Converter a coluna 'horario' para datetime
    df['horario'] = pd.to_datetime(df['horario'], format='%H:%M:%S', errors='coerce')

    # 2. Criar a coluna 'hora' a partir da coluna 'horario'
    df['hora'] = df['horario'].dt.hour

    # 3. Converter para inteiro compatível com valores nulos
    df['hora'] = df['hora'].astype('Int64')
    return df

def criar_coluna_regiao(df):
    regioes = {
    'AC': 'Norte', 'AP': 'Norte', 'AM': 'Norte', 'PA': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
    'MA': 'Nordeste', 'PI': 'Nordeste', 'CE': 'Nordeste', 'RN': 'Nordeste', 'PB': 'Nordeste',
    'PE': 'Nordeste', 'AL': 'Nordeste', 'SE': 'Nordeste', 'BA': 'Nordeste',
    'MG': 'Sudeste', 'ES': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
    'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul',
    'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'MS': 'Centro-Oeste'
    }

    df['Região'] = df['uf'].map(regioes)
    return df

def categoriza_via_com_curva(tracado):
    if not isinstance(tracado, str):
        return 'Outros'

    tracado = tracado.lower()

    if 'declive' in tracado:
        return 'Declive'
    elif 'aclive' in tracado:
        return 'Aclive'
    elif 'viaduto' in tracado:
        return 'Viaduto'
    elif 'curva' in tracado:  # Nova condição
        return 'Curva'
    elif 'reta' in tracado:
        return 'Reta'
    else:
        return 'Outros'
    
def ajustar_mapeamento_climatico(df):
    mapeamento_compacto = {
    'Céu Claro': 'Bom',
    'Sol': 'Bom',
    'Nublado': 'Bom',
    'Chuva': 'Chuva',
    'Garoa/Chuvisco': 'Chuva',
    'Vento': 'Outros',
    'Nevoeiro/Neblina': 'Outros',
    'Granizo': 'Outros',
    'Neve': 'Outros',
    'Ignorado': 'Outros'
}

    df['Condicao_Climatica_Grupo'] = df['condicao_metereologica'].map(mapeamento_compacto)
    return df

def ajustar_colunas_latitude_longitude(df):
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    return df

def agrupar_causa(causa):
    causa = str(causa).lower()

    if any(p in causa for p in ['reação', 'velocidade', 'contramão', 'ultrapassagem', 'preferência', 'faixa', 'racha', 'celular', 'distância']):
        return 'Condutor - Falha humana'
    elif any(p in causa for p in ['álcool', 'psicoativa', 'dormindo', 'mal súbito', 'suicídio', 'transtorno']):
        return 'Condutor - Fadiga/Álcool/Drogas/Saúde'
    elif any(p in causa for p in ['pista', 'burac', 'curva', 'declive', 'iluminação', 'sinalização', 'acostamento', 'drenagem', 'obras', 'via']):
        return 'Via / Infraestrutura'
    elif any(p in causa for p in ['chuva', 'neblina', 'fumaça', 'óleo', 'areia', 'fenômenos']):
        return 'Condições Climáticas / Ambiente'
    elif any(p in causa for p in ['freio', 'suspensão', 'pneu', 'mecânic', 'elétric', 'farol']):
        return 'Veículo - Falha mecânica'
    elif any(p in causa for p in ['pedestre']):
        return 'Pedestre'
    elif any(p in causa for p in ['animal', 'objeto', 'obstrução', 'assalto']):
        return 'Animais / Objetos / Obstáculos'
    else:
        return 'Outros / Indefinidos'

def  agregar_colunas_feridos(df):
    df['feridos'] = df['feridos_leves'] + df['feridos_graves']
    return df

def ajustar_coluna_municipios(df):
    df['municipio'] = df.apply(
    lambda x: f"{x['municipio']} - {x['uf']}" if pd.notna(x['uf']) and x['uf'] != '' else x['municipio'],
    axis=1
    )
    return df

def aplicar_Title(df):
    df.columns = [col.replace('_', ' ').title() for col in df.columns]
    return df

def ajustar_colunas_multiplas_objetic(df):
    # 2. APLICAR TITLE CASE NO CONTEÚDO DAS COLUNAS DE TEXTO
    # Seleciona as colunas de texto, exceto 'Uf'
    string_columns = df.select_dtypes(include=['object']).columns.drop('Uf', errors='ignore')

    # Aplica Title Case em todas as colunas de texto selecionadas
    for col in string_columns:
        df[col] = df[col].str.title()

    # Aplica a função .str.title() em todas as colunas de texto selecionadas
    # O .str garante que a operação só funcione em strings, ignorando valores nulos (NaN)
    df[string_columns] = df[string_columns].apply(lambda x: x.str.title())
    return df

def salvar(df):
    df.to_csv('PRF2023a2026.csv', index=False, sep=';', encoding='utf-8-sig')
    df.to_parquet('PRF2023a2026.parquet', index=False)  

    
# Função
def main():
    df = carregar_e_concatenar(ANOS, BASE_DIR)
    df = ajustar_coluna_data_inversa(df)
    df = gerar_colunas_derivadas_como_inteiros(df)
    df = criar_mapa_meses(df)
    df = alterar_nome_coluna_data_inversa(df)
    df = criar_coluna_partes_dia(df)
    df = converter_coluna_horario_para_datatime(df)
    df = criar_coluna_regiao(df)
    df['Grupo_via'] = df['tracado_via'].apply(categoriza_via_com_curva)
    df = ajustar_mapeamento_climatico(df) 
    df = ajustar_colunas_latitude_longitude(df)
    df['Causa_Grupo'] = df['causa_acidente'].apply(agrupar_causa)
    df = agregar_colunas_feridos(df)
    df = ajustar_coluna_municipios(df)
    df = aplicar_Title(df)
    df = ajustar_colunas_multiplas_objetic(df)
    salvar(df)
    print(df.head(5))
    print(df.tail(5))
# Executa o app

if __name__ == '__main__':
    main()
