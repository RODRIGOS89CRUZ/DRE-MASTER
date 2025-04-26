# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import time
import re
from fpdf import FPDF

# Função para limpar e padronizar nomes de colunas
def padronizar_nome(coluna):
    coluna = coluna.lower()
    coluna = re.sub(r'[^a-zA-Z0-9 ]', '', coluna)
    coluna = coluna.strip()
    return coluna

# Função para carregar o arquivo Excel do DRE
def carregar_dre(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        df.columns = [padronizar_nome(col) for col in df.columns]
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

# Mapeamento estruturado com base no modelo correto de um DRE
COLUNAS_PADRAO = {
    'receita_liquida': ['receita operacional liquida', 'receita liquida'],
    'custos_vendas': ['custos das vendas', 'custo dos produtos vendidos'],
    'lucro_liquido_exercicio': ['resultado liquido do exercicio', 'lucro liquido'],
    'margem_lucro': ['porcentagem de lucro liquido', 'margem de lucro'],
    'ebitda': ['ebitda', 'resultado operacional antes de depreciação e amortização'],
    'ebit': ['ebit', 'resultado operacional'],
    'fluxo_caixa': ['resultado bancario liquido fluxo de caixa', 'fluxo de caixa']
}

# Função utilitária para encontrar coluna no DataFrame
def encontrar_coluna(dre_df, opcoes):
    for opcao in opcoes:
        for coluna in dre_df.columns:
            if opcao in coluna:
                return coluna
    return None

# Função para gerar relatório em PDF
def gerar_pdf(receita_total, lucro_total, margem_media):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório de Análise de DRE", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Receita Líquida Total: R$ {receita_total:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Lucro Líquido Total: R$ {lucro_total:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Margem de Lucro Média: {margem_media:.2f}%", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Análises Adicionais (em breve)", ln=True)
    return pdf

# Função para salvar PDF em bytes
def salvar_pdf_em_bytes(pdf):
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

# Novo: Função de Inicialização
def iniciar_dashboard():
    st.title("📊 DreMaster - Inteligência Financeira Avançada")

    uploaded_file = st.sidebar.file_uploader("📂 Faça o upload do seu arquivo DRE (Excel)", type=["xlsx"])

    if uploaded_file:
        dre_df = carregar_dre(uploaded_file)

        if dre_df is not None:
            receita_col = encontrar_coluna(dre_df, COLUNAS_PADRAO['receita_liquida'])
            lucro_col = encontrar_coluna(dre_df, COLUNAS_PADRAO['lucro_liquido_exercicio'])
            margem_col = encontrar_coluna(dre_df, COLUNAS_PADRAO['margem_lucro'])

            if receita_col and lucro_col and margem_col:
                receita_total = dre_df[receita_col].sum()
                lucro_total = dre_df[lucro_col].sum()
                margem_media = dre_df[margem_col].mean()

                st.metric("Receita Líquida Total", f"R$ {receita_total:,.2f}")
                st.metric("Lucro Líquido Total", f"R$ {lucro_total:,.2f}")
                st.metric("Margem de Lucro Média", f"{margem_media:.2f}%")

                pdf = gerar_pdf(receita_total, lucro_total, margem_media)
                pdf_bytes = salvar_pdf_em_bytes(pdf)
                st.download_button(label="📄 Baixar Relatório em PDF", data=pdf_bytes, file_name="relatorio_dre.pdf", mime="application/pdf")

                st.success("Análise concluída com sucesso! Mais recursos avançados serão carregados na próxima fase.")
            else:
                st.warning("⚠️ Algumas colunas essenciais não foram encontradas no seu arquivo. Verifique o modelo utilizado.")

    else:
        st.info("Por favor, envie seu arquivo de DRE para iniciar a análise.")

# Rodar o app
iniciar_dashboard()
