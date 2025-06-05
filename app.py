
import streamlit as st
import pandas as pd
import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

st.set_page_config(page_title="Roleta com Scraping Corrigido", layout="centered")

# Sessão
if "historico" not in st.session_state:
    st.session_state.historico = []
if "saldo" not in st.session_state:
    st.session_state.saldo = 1000.0

st.title("🎯 Roleta Evolution com Scraping (Blaze) Corrigido")

# Função corrigida de scraping
def capturar_numero_blaze():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://blaze.com/pt/games/double")
        time.sleep(6)  # Aguarda carregar

        # Captura o último número da roleta
        bolas = driver.find_elements("class name", "entry")
        ultimos_numeros = [b.text.strip() for b in bolas if b.text.strip().isdigit()]

        driver.quit()

        if not ultimos_numeros:
            return "Não foi possível encontrar número na tela."

        return int(ultimos_numeros[-1])  # Pega o último número válido
    except Exception as e:
        driver.quit()
        return f"Erro: {e}"

# Botão para scraping
if st.button("📡 Capturar número ao vivo"):
    numero = capturar_numero_blaze()
    if isinstance(numero, int):
        st.session_state.historico.append({"numero": numero, "data": datetime.datetime.now()})
        st.success(f"Número capturado: {numero}")
    else:
        st.error(numero)

# Exibir histórico
if st.session_state.historico:
    df = pd.DataFrame(st.session_state.historico)
    df["Cor"] = df["numero"].apply(lambda x: "Verde" if x == 0 else "Vermelho" if x in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36] else "Preto")
    df["Par/Ímpar"] = df["numero"].apply(lambda x: "Zero" if x == 0 else "Par" if x % 2 == 0 else "Ímpar")

    st.subheader("📊 Últimos resultados")
    st.dataframe(df.tail(10))
else:
    st.info("Nenhum número capturado ainda.")
