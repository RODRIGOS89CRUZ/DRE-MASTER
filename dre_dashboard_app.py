# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import time

# Função para carregar o arquivo Excel do DRE
def carregar_dre(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        df.columns = df.columns.str.strip()  # Remove espaços
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

# Função para encontrar coluna válida a partir de lista de opções
def encontrar_coluna(dre_df, opcoes):
    for opcao in opcoes:
        if opcao in dre_df.columns:
            return opcao
    return None

# Mapeamento flexível de colunas esperadas
COLUNAS_PADRAO = {
    'receita': ['RECEITA MENSAL BANCÁRIA', 'Receita', 'Faturamento', 'Receita Total'],
    'custo': ['(-) CUSTOS DAS VENDAS', 'Custo', 'Custos Totais'],
    'lucro': ['(=) RESULTADO LÍQUIDO DO EXERCÍCIO', 'Lucro', 'Lucro Líquido']
}

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
    'RECEITA MENSAL BANCÁRIA': [10000, 12000, 11000],
    '(-) CUSTOS DAS VENDAS': [4000, 5000, 4500],
    '(=) RESULTADO LÍQUIDO DO EXERCÍCIO': [6000, 7000, 6500],
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

            col_receita = encontrar_coluna(dre_df, COLUNAS_PADRAO['receita'])
            col_custo = encontrar_coluna(dre_df, COLUNAS_PADRAO['custo'])
            col_lucro = encontrar_coluna(dre_df, COLUNAS_PADRAO['lucro'])

            if all([col_receita, col_custo, col_lucro]):
                receita_total = dre_df[col_receita].sum()
                custo_total = dre_df[col_custo].sum()
                lucro_total = dre_df[col_lucro].sum()
                margem = (lucro_total / receita_total) * 100 if receita_total else 0

                status = "🟢 Saudável" if margem >= 10 else "🔴 Alerta: Margem Baixa"

                st.success("✅ Arquivo carregado com sucesso!")

                st.markdown(f"""
                    <div style='background-color: #ecf0f1; padding: 20px; border-radius: 10px;'>
                        <h3 style='color: #2c3e50;'>📋 Resumo do Negócio</h3>
                        <p><b>Receita Total:</b> R$ {receita_total:,.2f}</p>
                        <p><b>Lucro Total:</b> R$ {lucro_total:,.2f}</p>
                        <p><b>Margem de Lucro:</b> {margem:.2f}%</p>
                        <p><b>Status:</b> {status}</p>
                    </div>
                """, unsafe_allow_html=True)

                st.divider()
                criar_dashboard(dre_df)

                st.divider()

                # Gráficos de Pizza Receita e Despesa
                st.subheader("📊 Análise de Receita e Despesa por Categoria")
                col1, col2 = st.columns(2)

                with col1:
                    if 'Tipo Receita' in dre_df.columns:
                        receita_tipo = dre_df.groupby('Tipo Receita')[col_receita].sum()
                        fig1, ax1 = plt.subplots()
                        ax1.pie(receita_tipo, labels=receita_tipo.index, autopct='%1.1f%%', startangle=90)
                        ax1.axis('equal')
                        st.pyplot(fig1)

                with col2:
                    if 'Tipo Despesa' in dre_df.columns:
                        despesa_tipo = dre_df.groupby('Tipo Despesa')[col_custo].sum()
                        fig2, ax2 = plt.subplots()
                        ax2.pie(despesa_tipo, labels=despesa_tipo.index, autopct='%1.1f%%', startangle=90)
                        ax2.axis('equal')
                        st.pyplot(fig2)

                st.divider()

                # Gráfico Comparativo Lucro Mês a Mês
                st.subheader("📈 Lucro Mensal: Evolução ao longo do tempo")
                if 'Período' in dre_df.columns and col_lucro in dre_df.columns:
                    fig3, ax3 = plt.subplots(figsize=(10,5))
                    ax3.plot(dre_df['Período'], dre_df[col_lucro], marker='o', linestyle='-', color='#1f77b4')
                    ax3.set_title('Lucro Mensal')
                    ax3.set_xlabel('Período')
                    ax3.set_ylabel('Lucro (R$)')
                    ax3.grid(True)
                    st.pyplot(fig3)
            else:
                st.error("⚠️ Não foi possível identificar colunas de Receita, Custo ou Lucro no arquivo enviado. Verifique se o layout está correto.")
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
