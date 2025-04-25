# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Função para carregar o arquivo Excel
def carregar_dre(uploaded_file):
    if uploaded_file:
        return pd.read_excel(uploaded_file, engine='openpyxl')
    return None

# Função para criar dashboard
def criar_dashboard(dre_df):
    st.markdown("## 📊 Dashboard Financeiro", unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if 'Receita' in dre_df.columns and 'Lucro' in dre_df.columns:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(dre_df['Período'], dre_df['Receita'], marker='o', label='Receita')
            ax.plot(dre_df['Período'], dre_df['Lucro'], marker='o', label='Lucro')
            ax.set_xlabel('Período')
            ax.set_ylabel('Valores (R$)')
            ax.set_title('Receita vs Lucro')
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)

    with col2:
        if 'Custo' in dre_df.columns:
            st.markdown("### 📉 Custos por Período")
            st.bar_chart(dre_df.set_index('Período')['Custo'])

    st.divider()

    if 'Lucro' in dre_df.columns and 'Receita' in dre_df.columns:
        st.markdown("### 📈 Margem de Lucro (%)")
        dre_df['Margem (%)'] = (dre_df['Lucro'] / dre_df['Receita']) * 100
        st.line_chart(dre_df.set_index('Período')['Margem (%)'])

# App principal
st.set_page_config(page_title="DreMaster - Inteligência Financeira", layout="wide", page_icon="📊")

st.markdown("""
<style>
    .main {
        background-color: #f9f9f9;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("📈 DreMaster: Seu DRE, Sua Inteligência Financeira")

with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/000000/financial-growth-analysis.png", width=100)
    st.markdown("## 🔑 Configurações")
    uploaded_file = st.file_uploader("📂 Envie seu arquivo Excel do DRE", type=["xlsx"])

if uploaded_file:
    dre_df = carregar_dre(uploaded_file)

    if dre_df is not None:
        st.success("✅ Arquivo carregado com sucesso!")
        st.dataframe(dre_df, use_container_width=True)

        if st.button("📊 Gerar Dashboard"):
            with st.spinner("⏳ Gerando visualizações..."):
                criar_dashboard(dre_df)
else:
    st.info("🔹 Para começar, envie um arquivo do DRE na barra lateral.")
