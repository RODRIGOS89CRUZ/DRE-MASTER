# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import time

# Função para carregar o arquivo Excel do DRE
def carregar_dre(uploaded_file):
    try:
        return pd.read_excel(uploaded_file, engine='openpyxl')
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

# (Todas as funções que você já criou permanecem aqui, conforme estão)
# gerar_relatorio, gerar_analise, gerar_insights_avancados, analisar_tendencias, criar_dashboard

# Código principal para rodar o app
st.set_page_config(page_title="DreMaster - Dashboard Financeiro", layout="wide")

# Adicionando logotipo e cabeçalho
st.markdown("""
    <div style='text-align: center;'>
        <img src='https://img.icons8.com/ios-filled/100/financial-growth-analysis.png' width='120'/>
        <h1 style='color: #2c3e50; font-family: Arial, sans-serif;'>📈 DreMaster: Plataforma Inteligente de DRE</h1>
    </div>
""", unsafe_allow_html=True)

st.divider()

# Botão para baixar exemplo de arquivo
example_data = pd.DataFrame({
    'Período': ['Jan', 'Feb', 'Mar'],
    'Receita': [10000, 12000, 11000],
    'Custo': [4000, 5000, 4500],
    'Lucro': [6000, 7000, 6500],
    'Tipo Receita': ['Produto A', 'Produto B', 'Produto A'],
    'Tipo Despesa': ['Fixo', 'Variável', 'Fixo']
})
example_file = BytesIO()
with pd.ExcelWriter(example_file, engine='openpyxl') as writer:
    example_data.to_excel(writer, index=False, sheet_name='DRE')
example_file.seek(0)

st.sidebar.download_button(
    label="📄 Baixar exemplo de DRE",
    data=example_file,
    file_name="exemplo_dre.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Upload de arquivo do usuário
uploaded_file = st.sidebar.file_uploader("📂 Faça upload do seu DRE em Excel", type=["xlsx"])

if uploaded_file:
    dre_df = carregar_dre(uploaded_file)

    if dre_df is not None:
        with st.spinner("🔄 Analisando seu DRE e preparando os gráficos..."):
            time.sleep(2)
            st.success("✅ Arquivo carregado com sucesso!")

            # Visão Geral do Negócio
            receita_total = dre_df['Receita'].sum()
            custo_total = dre_df['Custo'].sum()
            lucro_total = dre_df['Lucro'].sum()
            margem = (lucro_total / receita_total) * 100 if receita_total else 0

            status = "🟢 Saudável" if margem >= 10 else "🔴 Alerta: Margem Baixa"

            st.markdown("""
                <div style='background-color: #ecf0f1; padding: 20px; border-radius: 10px;'>
                    <h3 style='color: #2c3e50;'>📋 Resumo do Negócio</h3>
                    <p><b>Receita Total:</b> R$ {:.2f}</p>
                    <p><b>Lucro Total:</b> R$ {:.2f}</p>
                    <p><b>Margem de Lucro:</b> {:.2f}%</p>
                    <p><b>Status:</b> {}</p>
                </div>
            """.format(
                receita_total,
                lucro_total,
                margem,
                status
            ), unsafe_allow_html=True)

            st.divider()

            criar_dashboard(dre_df)

            st.divider()

            # Gráficos de Pizza Receita e Despesa
            st.subheader("📊 Análise de Receita e Despesa por Categoria")
            col1, col2 = st.columns(2)

            with col1:
                if 'Tipo Receita' in dre_df.columns:
                    receita_tipo = dre_df.groupby('Tipo Receita')['Receita'].sum()
                    fig1, ax1 = plt.subplots()
                    ax1.pie(receita_tipo, labels=receita_tipo.index, autopct='%1.1f%%', startangle=90)
                    ax1.axis('equal')
                    st.pyplot(fig1)

            with col2:
                if 'Tipo Despesa' in dre_df.columns:
                    despesa_tipo = dre_df.groupby('Tipo Despesa')['Custo'].sum()
                    fig2, ax2 = plt.subplots()
                    ax2.pie(despesa_tipo, labels=despesa_tipo.index, autopct='%1.1f%%', startangle=90)
                    ax2.axis('equal')
                    st.pyplot(fig2)

            st.divider()

            # Gráfico Comparativo Lucro Mês a Mês
            st.subheader("📈 Lucro Mensal: Evolução ao longo do tempo")
            if 'Período' in dre_df.columns and 'Lucro' in dre_df.columns:
                fig3, ax3 = plt.subplots(figsize=(10,5))
                ax3.plot(dre_df['Período'], dre_df['Lucro'], marker='o', linestyle='-', color='#1f77b4')
                ax3.set_title('Lucro Mensal')
                ax3.set_xlabel('Período')
                ax3.set_ylabel('Lucro (R$)')
                ax3.grid(True)
                st.pyplot(fig3)
else:
    st.info("📥 Comece enviando seu DRE na barra lateral ou baixe o exemplo para testar agora.")

# Estilo adicional
st.markdown("""
<style>
    .stButton>button {
        background-color: #2c3e50;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stDownloadButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)
