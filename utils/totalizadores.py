import pandas as pd


def total_acidentes(df):
    return f" {formatar_milhar(len(df))}"

def total_mortos(df):
    return f"{formatar_milhar(df['Mortos'].sum())}"

def total_feridos(df):
    return f"{formatar_milhar(df['Feridos'].sum())}"

def total_veiculos(df):
    return f"{formatar_milhar(df['Veiculos'].sum())}"

#def total_ilesos(df):
   # return f"{formatar_milhar(df['Ilesos'].sum())}"


def formatar_milhar(valor):
    if isinstance(valor, (pd.Series, list)):
        return [formatar_milhar(v) for v in valor]
    if pd.isna(valor):
        return 0
    return f"{int(valor):,}".replace(",", ".")


def calculo_tot_acidentes(df):
    return len(df)

def calculo_tot_mortos(df):
    return df['Mortos'].sum()

def calculo_tot_feridos(df):
    return df['Feridos'].sum()

def calculo_tot_veiculos(df):
    return df['Veiculos'].sum()




