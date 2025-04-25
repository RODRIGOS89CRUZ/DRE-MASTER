# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from scipy.signal import find_peaks

# Função para carregar o arquivo Excel
def carregar_dre(uploaded_file):
    try:
        if uploaded_file:
            return pd.read_excel(uploaded_file, engine='openpyxl')
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
    return None

# Função para criar e baixar o relatório em Excel
def gerar_relatorio(dre_df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        dre_df.to_excel(writer, sheet_name='DRE', index=False)
    return output.getvalue()

# Função para gerar análise textual simples
def gerar_analise(dre_df):
    texto = ""
    receita_total = dre_df['Receita'].sum() if 'Receita' in dre_df.columns else 0
    custo_total = dre_df['Custo'].sum() if 'Custo' in dre_df.columns else 0
    lucro_total = dre_df['Lucro'].sum() if 'Lucro' in dre_df.columns else 0
    margem_media = (lucro_total / receita_total) * 100 if receita_total else 0

    if receita_total == 0:
        texto += "🔸 Receita zerada: é necessário revisar seu plano de vendas.\n"
    elif margem_media < 10:
        texto += "🔸 Margem muito baixa: considere reduzir custos fixos e renegociar fornecedores.\n"
    elif margem_media >= 10 and margem_media < 20:
        texto += "🔸 Margem moderada: boas práticas, mas atenção ao aumento de despesas.\n"
    else:
        texto += "🔸 Margem excelente: aproveite para reinvestir no crescimento.\n"

    if custo_total > receita_total:
        texto += "🔸 Alerta: custos maiores que a receita! Corte despesas urgentes.\n"

    return texto

# Função para gerar insights e aconselhamentos avançados
def gerar_insights_avancados(dre_df):
    insights = "\n\n🔮 **Insights Estratégicos Avançados:**\n"
    if 'Receita' in dre_df.columns and 'Custo' in dre_df.columns:
        receita_variacao = dre_df['Receita'].pct_change().mean() * 100
        custo_variacao = dre_df['Custo'].pct_change().mean() * 100
        margem_atual = ((dre_df['Lucro'].iloc[-1] / dre_df['Receita'].iloc[-1]) * 100) if dre_df['Receita'].iloc[-1] else 0

        if receita_variacao > 5:
            insights += "✅ Receita crescendo consistentemente: invista em expansão e inovação.\n"
        elif receita_variacao < -5:
            insights += "⚠️ Receita em queda: reavalie estratégia comercial e marketing.\n"

        if custo_variacao > receita_variacao:
            insights += "⚠️ Custos crescendo acima da receita: atenção urgente ao controle de despesas.\n"

        if margem_atual < 10:
            insights += "⚠️ Margem muito baixa: revisar preços, renegociar fornecedores ou reduzir custos operacionais.\n"
        elif margem_atual > 20:
            insights += "✅ Margem excelente: possibilidade de reinvestir ou expandir operações.\n"

        if (dre_df['Receita'] > dre_df['Custo']).all():
            insights += "✅ Receita consistentemente maior que o custo: fluxo de caixa saudável.\n"
        else:
            insights += "⚠️ Há meses com custos superiores à receita: atenção à gestão de caixa.\n"

    return insights

# Função para detectar tendências e padrões
def analisar_tendencias(dre_df):
    texto = "\n\n🔍 **Análise de Tendências:**\n"
    if 'Receita' in dre_df.columns and 'Custo' in dre_df.columns:
        fluxo = (dre_df['Receita'] - dre_df['Custo']).cumsum()
        fluxo_diff = fluxo.diff().fillna(0)

        # Encontrar picos de alta e baixa
        picos, _ = find_peaks(fluxo_diff)
        vales, _ = find_peaks(-fluxo_diff)

        if len(picos) > 0:
            texto += f"🔹 Foram encontrados {len(picos)} períodos de crescimento acentuado de caixa.\n"
        if len(vales) > 0:
            texto += f"🔹 Foram identificados {len(vales)} períodos de queda significativa no fluxo de caixa.\n"

        if fluxo_diff.mean() > 0:
            texto += "🔹 Tendência geral: crescimento financeiro positivo ao longo do tempo.\n"
        else:
            texto += "🔹 Tendência geral: alerta de tendência de queda no fluxo financeiro.\n"
    return texto

# Função para criar dashboard melhorado
def criar_dashboard(dre_df):
    st.markdown("# 📊 Painel Financeiro - DreMaster", unsafe_allow_html=True)
    st.divider()

    # KPIs principais
    receita_total = dre_df['Receita'].sum() if 'Receita' in dre_df.columns else 0
    custo_total = dre_df['Custo'].sum() if 'Custo' in dre_df.columns else 0
    lucro_total = dre_df['Lucro'].sum() if 'Lucro' in dre_df.columns else 0
    margem_media = (lucro_total / receita_total) * 100 if receita_total else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Receita Total", f"R$ {receita_total:,.2f}")
    col2.metric("Custo Total", f"R$ {custo_total:,.2f}")
    col3.metric("Lucro Total", f"R$ {lucro_total:,.2f}")
    col4.metric("Margem Média", f"{margem_media:.2f}%")

    st.divider()

    # Gráficos Receita vs Lucro
    if 'Receita' in dre_df.columns and 'Lucro' in dre_df.columns:
        st.subheader("📈 Receita vs Lucro")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(dre_df['Período'], dre_df['Receita'], marker='o', linestyle='-', label='Receita', color='#1f77b4')
        ax.plot(dre_df['Período'], dre_df['Lucro'], marker='s', linestyle='--', label='Lucro', color='#2ca02c')
        ax.fill_between(dre_df['Período'], dre_df['Receita'], dre_df['Lucro'], color='#d3d3d3', alpha=0.3)
        ax.set_xlabel('Período')
        ax.set_ylabel('Valores (R$)')
        ax.set_title('Receita e Lucro - Evolução')
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

    st.divider()

    # Gráfico de Custos
    if 'Custo' in dre_df.columns:
        st.subheader("📉 Evolução dos Custos")
        fig, ax = plt.subplots(figsize=(12, 6))
        cores = ['#FF4136' if v > 0 else '#2ECC40' for v in dre_df['Custo'].diff().fillna(0)]
        ax.bar(dre_df['Período'], dre_df['Custo'], color=cores)
        ax.set_xlabel('Período')
        ax.set_ylabel('Custos (R$)')
        ax.set_title('Custos por Período')
        st.pyplot(fig)

    st.divider()

    # Fluxo de Caixa Acumulado
    if 'Receita' in dre_df.columns and 'Custo' in dre_df.columns:
        st.subheader("💸 Fluxo de Caixa Acumulado")
        fluxo_caixa = (dre_df['Receita'] - dre_df['Custo']).cumsum()
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(dre_df['Período'], fluxo_caixa, marker='D', linestyle='-', color='#4682B4')
        ax.set_xlabel('Período')
        ax.set_ylabel('R$')
        ax.set_title('Fluxo de Caixa Acumulado')
        ax.grid(True)
        st.pyplot(fig)

    st.divider()

    # Botão para download do relatório
    relatorio = gerar_relatorio(dre_df)
    st.download_button(
        label="📥 Baixar Relatório Excel",
        data=relatorio,
        file_name="dre_relatorio.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Mostrar análise simples
    st.subheader("🧠 Análise e Recomendações")
    st.info(gerar_analise(dre_df))

    # Mostrar análise de tendências
    st.subheader("📊 Análise de Tendências e Padrões")
    st.success(analisar_tendencias(dre_df))

    # Mostrar insights avançados
    st.subheader("🔮 Insights Estratégicos Avançados")
    st.success(gerar_insights_avancados(dre_df))
