
import streamlit as st
import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt
import seaborn as sns

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

st.set_page_config(page_title="Roleta Betano - Scraping Real", layout="centered")
st.title("🎯 Roleta ao Vivo - Betano (Scraping Real)")

if "resultados" not in st.session_state:
    st.session_state.resultados = []

# Função de scraping real
def capturar_numero_betano():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        url = "https://www.betano.bet.br/casino/live/games/immersive-roulette/1527/tables/"
        driver.get(url)
        time.sleep(10)  # Aguarda a página carregar completamente

        xpath = '//*[@id="root"]/div/div/div[2]/div[8]/div[1]/div/div/div[2]/div/div/ul/li[3]/div'
        elemento = driver.find_element(By.XPATH, xpath)
        texto = elemento.text.strip()

        numero = int(texto)
        return numero
    except Exception as e:
        st.error(f"Erro ao capturar número: {e}")
        return None
    finally:
        driver.quit()

# Botão para capturar número real
if st.button("🎰 Capturar número da Betano (Roleta Imersiva)"):
    numero = capturar_numero_betano()
    if numero is not None:
        st.session_state.resultados.append({
            "numero": numero,
            "fonte": "Betano",
            "hora": datetime.datetime.now()
        })

# Exibe resultados e gráficos
if st.session_state.resultados:
    df = pd.DataFrame(st.session_state.resultados)
    df["cor"] = df["numero"].apply(lambda x: "Verde" if x == 0 else "Vermelho" if x in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36] else "Preto")
    df["paridade"] = df["numero"].apply(lambda x: "Zero" if x == 0 else "Par" if x % 2 == 0 else "Ímpar")
    df["dúzia"] = df["numero"].apply(lambda x: "0" if x == 0 else "1ª" if x <= 12 else "2ª" if x <= 24 else "3ª")

    st.subheader("📋 Últimos números")
    st.dataframe(df.tail(20))

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

    st.download_button("📥 Exportar CSV", data=df.to_csv(index=False), file_name="resultados_roleta.csv", mime="text/csv")

else:
    st.info("Nenhum número capturado ainda.")
