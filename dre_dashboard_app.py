import streamlit as st
import pandas as pd
import openai
import matplotlib.pyplot as plt
from io import BytesIO

# Função para carregar o arquivo Excel
def carregar_dre(uploaded_file):
    if uploaded_file:
        return pd.read_excel(uploaded_file)
    return None

# Função para gerar análise com GPT
def gerar_analise(dre_df, openai_api_key):
    openai.api_key = openai_api_key
    prompt = f"""
    Analise o seguinte Demonstrativo de Resultados do Exercício (DRE) e forneça insights sobre o desempenho financeiro, pontos fortes, pontos de atenção e sugestões de melhoria:

    {dre_df.to_string(index=False)}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Função para criar dashboard
def criar_dashboard(dre_df):
    st.subheader("\ud83d\udcca Dashboard Financeiro")

    if 'Receita' in dre_df.columns and 'Lucro' in dre_df.columns:
        fig, ax = plt.subplots()
        ax.plot(dre_df['Período'], dre_df['Receita'], marker='o', label='Receita')
        ax.plot(dre_df['Período'], dre_df['Lucro'], marker='o', label='Lucro')
        ax.set_xlabel('Período')
        ax.set_ylabel('Valores (R$)')
        ax.set_title('Receita e Lucro ao longo do tempo')
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

    if 'Custo' in dre_df.columns:
        st.subheader("Custos por Período")
        st.bar_chart(dre_df.set_index('Período')['Custo'])

    if 'Lucro' in dre_df.columns and 'Receita' in dre_df.columns:
        st.subheader("Margem de Lucro (%) por Período")
        dre_df['Margem (%)'] = (dre_df['Lucro'] / dre_df['Receita']) * 100
        st.line_chart(dre_df.set_index('Período')['Margem (%)'])

# App principal
st.set_page_config(page_title="DreMaster - Inteligência Financeira", layout="wide", page_icon="\ud83d\udcca")
st.title("\ud83d\udcc8 DreMaster: Seu DRE, Sua Inteligência Financeira")

with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/000000/financial-growth-analysis.png", width=100)
    st.header("\ud83d\udd11 Configurações")
    openai_api_key = st.text_input("Insira sua OpenAI API Key (opcional para análise GPT)", type="password")
    uploaded_file = st.file_uploader("\ud83d\udcc2 Envie seu arquivo Excel do DRE", type=["xlsx"])

if uploaded_file:
    dre_df = carregar_dre(uploaded_file)

    if dre_df is not None:
        st.success("Arquivo carregado com sucesso!")
        st.dataframe(dre_df, use_container_width=True)

        if st.button("\ud83d\udcca Gerar Dashboard e Análise"):
            with st.spinner("\u23f3 Gerando análise e visualizações..."):
                criar_dashboard(dre_df)

                if openai_api_key:
                    analise = gerar_analise(dre_df, openai_api_key)
                    st.subheader("\ud83d\udd0d Análise GPT")
                    st.write(analise)
                else:
                    st.info("\ud83d\udd39 Chave da API não fornecida: exibindo apenas o Dashboard.")
else:
    st.info("\ud83d\udd39 Para começar, envie um arquivo do DRE na barra lateral.")
