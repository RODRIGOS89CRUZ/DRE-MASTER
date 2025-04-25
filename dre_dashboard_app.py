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
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

# Mapeamento estruturado com base no modelo correto de um DRE
COLUNAS_PADRAO = {
    'receita_bruta': ['RECEITA MENSAL BANCÁRIA', 'RECEITA OPERACIONAL BRUTA'],
    'deducoes': ['(-) DEDUÇÕES DA RECEITA BRUTA'],
    'receita_liquida': ['= RECEITA OPERACIONAL LÍQUIDA'],
    'custos_vendas': ['(-) CUSTOS DAS VENDAS'],
    'resultado_operacional_bruto': ['= RESULTADO OPERACIONAL BRUTO'],
    'despesas_operacionais': ['(-) DESPESAS OPERACIONAIS'],
    'despesas_financeiras': ['(-) DESPESAS FINANCEIRAS LÍQUIDAS'],
    'outras_receitas_despesas': ['OUTRAS RECEITAS E DESPESAS'],
    'resultado_operacional_antes_ir': ['= RESULTADO OPERACIONAL ANTES DO IR E CSLL'],
    'lucro_antes_participacoes': ['= LUCRO LÍQUIDO ANTES DAS PARTICIPAÇÕES'],
    'pro_labore': ['(-) PRO LABORE'],
    'lucro_liquido_exercicio': ['(=) RESULTADO LÍQUIDO DO EXERCÍCIO'],
    'fluxo_caixa': ['(=) RESULTADO BANCÁRIO - LÍQUIDO - FLUXO DE CAIXA'],
    'ebit': ['Resultado Operacional (Ebit)'],
    'ebitda': ['EBITDA (Ebit+Depreciações)'],
    'resultado_final': ['Resultado Final'],
    'margem_lucro': ['PORCENTAGEM DE LUCRO LÍQUIDO (%)']
}

# Função utilitária para encontrar coluna no DataFrame
def encontrar_coluna(dre_df, opcoes):
    for opcao in opcoes:
        if opcao in dre_df.columns:
            return opcao
    return None

# Função para gerar relatórios e insights

def gerar_relatorio(dre_df):
    receita_col = encontrar_coluna(dre_df, COLUNAS_PADRAO['receita_liquida'])
    lucro_col = encontrar_coluna(dre_df, COLUNAS_PADRAO['lucro_liquido_exercicio'])
    margem_col = encontrar_coluna(dre_df, COLUNAS_PADRAO['margem_lucro'])

    if receita_col and lucro_col and margem_col:
        receita = dre_df[receita_col].sum()
        lucro = dre_df[lucro_col].sum()
        margem = dre_df[margem_col].mean()

        st.subheader("📋 Relatório de Desempenho")
        st.write(f"Receita Líquida Total: R$ {receita:,.2f}")
        st.write(f"Lucro Líquido Total: R$ {lucro:,.2f}")
        st.write(f"Margem Média de Lucro: {margem:.2f}%")

        st.subheader("💡 Insights Estratégicos")
        if margem >= 20:
            st.success("Ótima margem de lucro! Continue mantendo o controle de despesas e otimize ainda mais suas operações.")
        elif 10 <= margem < 20:
            st.warning("Margem de lucro razoável. Avalie estratégias para aumentar a eficiência e reduzir custos.")
        else:
            st.error("Margem de lucro baixa! Reavalie urgências: custos elevados, necessidade de aumento de vendas ou ajuste de preços.")

# Função para mostrar KPIs, gráficos e relatórios do DRE
def mostrar_kpis(dre_df):
    st.title("📊 Análise de DRE - Dashboard")

    col_receita = encontrar_coluna(dre_df, COLUNAS_PADRAO['receita_liquida'])
    col_lucro = encontrar_coluna(dre_df, COLUNAS_PADRAO['lucro_liquido_exercicio'])
    col_margem = encontrar_coluna(dre_df, COLUNAS_PADRAO['margem_lucro'])

    if not (col_receita or col_lucro or col_margem):
        st.warning("⚠️ Não foi possível encontrar colunas de Receita Líquida, Lucro Líquido ou Margem de Lucro no seu arquivo. Verifique o layout.")
        return

    colunas_kpi = st.columns(3)

    with colunas_kpi[0]:
        if col_receita:
            receita_total = dre_df[col_receita].sum()
            st.metric("Receita Líquida", f"R$ {receita_total:,.2f}")

    with colunas_kpi[1]:
        if col_lucro:
            lucro_total = dre_df[col_lucro].sum()
            st.metric("Lucro Líquido", f"R$ {lucro_total:,.2f}")

    with colunas_kpi[2]:
        if col_margem:
            margem_media = dre_df[col_margem].mean()
            st.metric("Margem de Lucro (%)", f"{margem_media:.2f}%")

    st.divider()

    st.subheader("📈 Gráficos Financeiros")

    if col_receita and (col_custo := encontrar_coluna(dre_df, COLUNAS_PADRAO['custos_vendas'])):
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(['Receita Líquida', 'Custos'], [dre_df[col_receita].sum(), dre_df[col_custo].sum()], color=['#2ecc71', '#e74c3c'])
        ax.set_ylabel('Valor (R$)')
        st.pyplot(fig)
    else:
        st.info("ℹ️ Não há dados suficientes para o gráfico de Receita vs Custos.")

    col_desp_op = encontrar_coluna(dre_df, COLUNAS_PADRAO['despesas_operacionais'])
    col_desp_fin = encontrar_coluna(dre_df, COLUNAS_PADRAO['despesas_financeiras'])
    if col_desp_op and col_desp_fin:
        fig2, ax2 = plt.subplots()
        valores = [dre_df[col_desp_op].sum(), dre_df[col_desp_fin].sum()]
        labels = ['Despesas Operacionais', 'Despesas Financeiras']
        ax2.pie(valores, labels=labels, autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')
        st.pyplot(fig2)
    else:
        st.info("ℹ️ Não há dados suficientes para o gráfico de despesas.")

    if 'Período' in dre_df.columns and col_receita and col_lucro:
        st.subheader("📈 Tendência de Receita e Lucro ao longo do Tempo")
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        ax3.plot(dre_df['Período'], dre_df[col_receita], label='Receita Líquida', marker='o')
        ax3.plot(dre_df['Período'], dre_df[col_lucro], label='Lucro Líquido', marker='s')
        ax3.set_xlabel('Período')
        ax3.set_ylabel('Valor (R$)')
        ax3.legend()
        ax3.grid(True)
        st.pyplot(fig3)

        tendencia_receita = "crescente" if dre_df[col_receita].iloc[-1] > dre_df[col_receita].iloc[0] else "decrescente"
        tendencia_lucro = "crescente" if dre_df[col_lucro].iloc[-1] > dre_df[col_lucro].iloc[0] else "decrescente"

        st.info(f"📈 Tendência de Receita: {tendencia_receita.capitalize()}\n\n📈 Tendência de Lucro: {tendencia_lucro.capitalize()}")
    else:
        st.info("ℹ️ Tendência não disponível: coluna 'Período' ou dados insuficientes.")

    gerar_relatorio(dre_df)

# Código principal
uploaded_file = st.sidebar.file_uploader("📂 Envie o seu arquivo de DRE", type=["xlsx"])

if uploaded_file:
    dre_df = carregar_dre(uploaded_file)

    if dre_df is not None:
        mostrar_kpis(dre_df)
else:
    st.info("📥 Faça upload de um arquivo Excel (.xlsx) com os dados do seu DRE para iniciar a análise.")
