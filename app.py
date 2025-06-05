
import streamlit as st
import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt
import seaborn as sns

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

st.set_page_config(page_title="Análise Avançada - Roleta", layout="centered")
st.title("🎯 Simulador Roleta com Scraping (Betano + Evolution)")

# Inicializa sessão
if "resultados" not in st.session_state:
    st.session_state.resultados = []

# Função de scraping simulada (ajustar seletor real depois)
def capturar_numero_fake(site):
    # Aqui o Selenium real será implementado depois para Betano e Evolution
    import random
    return random.choice(list(range(0, 37)))

# Captura
col1, col2 = st.columns(2)
with col1:
    if st.button("🎰 Capturar número - Betano"):
        numero = capturar_numero_fake("betano")
        st.session_state.resultados.append({
            "numero": numero,
            "fonte": "Betano",
            "hora": datetime.datetime.now()
        })
with col2:
    if st.button("🎥 Capturar número - Evolution"):
        numero = capturar_numero_fake("evolution")
        st.session_state.resultados.append({
            "numero": numero,
            "fonte": "Evolution",
            "hora": datetime.datetime.now()
        })

# Mostra resultados
if st.session_state.resultados:
    df = pd.DataFrame(st.session_state.resultados)
    df["cor"] = df["numero"].apply(lambda x: "Verde" if x == 0 else "Vermelho" if x in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36] else "Preto")
    df["paridade"] = df["numero"].apply(lambda x: "Zero" if x == 0 else "Par" if x % 2 == 0 else "Ímpar")
    df["dúzia"] = df["numero"].apply(lambda x: "0" if x == 0 else "1ª" if x <= 12 else "2ª" if x <= 24 else "3ª")

    st.subheader("📋 Últimos números")
    st.dataframe(df.tail(20))

    # Gráficos
    st.subheader("📊 Frequência por número")
    fig1, ax1 = plt.subplots(figsize=(10,3))
    sns.countplot(x="numero", data=df, palette="viridis", ax=ax1)
    st.pyplot(fig1)

    st.subheader("🎨 Frequência por cor")
    fig2, ax2 = plt.subplots()
    sns.countplot(x="cor", data=df, palette={"Vermelho": "red", "Preto": "black", "Verde": "green"}, ax=ax2)
    st.pyplot(fig2)

    st.subheader("🧮 Frequência por paridade")
    fig3, ax3 = plt.subplots()
    sns.countplot(x="paridade", data=df, palette="Set2", ax=ax3)
    st.pyplot(fig3)

    st.subheader("📦 Frequência por dúzia")
    fig4, ax4 = plt.subplots()
    sns.countplot(x="dúzia", data=df, palette="Set1", ax=ax4)
    st.pyplot(fig4)

    # Exportação
    st.download_button("📥 Exportar CSV", data=df.to_csv(index=False), file_name="resultados_roleta.csv", mime="text/csv")

else:
    st.info("Nenhum número capturado ainda.")
