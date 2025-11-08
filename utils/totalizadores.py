import pandas as pd


# Cálculo do período do df
def calculo_data_final_df(df, coluna):
    return df[coluna].max().strftime("%d/%m/%Y") if not df.empty else None

def calculo_data_inicial_df(df, coluna):
    return df[coluna].min().strftime("%d/%m/%Y") if not df.empty else None


# Cáculo de totalizadores
def total_acidentes(df):
    return f" {formatar_milhar(len(df))}"

def total_mortos(df):
    return f"{formatar_milhar(df['Mortos'].sum())}"

def total_feridos(df):
    return f"{formatar_milhar(df['Feridos'].sum())}"

def total_veiculos(df):
    return f"{formatar_milhar(df['Veiculos'].sum())}"

def calculo_tot_acidentes(df):
    return len(df)

def calculo_tot_mortos(df):
    return df['Mortos'].sum()

def calculo_tot_feridos(df):
    return df['Feridos'].sum()

def calculo_tot_veiculos(df):
    return df['Veiculos'].sum()


# Formatação
def formatar_milhar(valor):
    if isinstance(valor, (pd.Series, list)):
        return [formatar_milhar(v) for v in valor]
    if pd.isna(valor):
        return 0
    return f"{int(valor):,}".replace(",", ".")




