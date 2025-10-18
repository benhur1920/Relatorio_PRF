# utils/dataframe.py
import streamlit as st

def mainDataframe(df):
    st.title("Visualização do DataFrame")
    st.dataframe(df)
