
import streamlit as st
import pandas as pd
import datetime
import base64
import time
import os

st.set_page_config(page_title="Roleta Avançada", layout="centered")

# 🌙 Tema adaptativo (auto)
st.markdown(
    """
    <style>
    html[data-theme="light"] {
        --main-bg-color: #ffffff;
    }
    html[data-theme="dark"] {
        --main-bg-color: #0e1117;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sessão
if "historico" not in st.session_state:
    st.session_state.historico = []
if "saldo" not in st.session_state:
    st.session_state.saldo = 1000.0

# 🎞️ Animação (roleta girando)
with st.expander("🎞️ Ver animação da roleta"):
    st.image("https://media.tenor.com/VaJMN9M42kUAAAAC/roulette.gif")

st.title("🎰 Simulador Avançado - Roleta Evolution")

# Inserção manual
numero = st.number_input("🎯 Número sorteado (0-36)", 0, 36, step=1)
if st.button("Adicionar número"):
    st.session_state.historico.append({"numero": numero, "data": datetime.datetime.now()})
    st.success(f"Número {numero} adicionado com sucesso!")
    # 🎵 Som simulado (placeholder)
    st.audio("https://www.myinstants.com/media/sounds/win.mp3")

# Reset
if st.button("🔄 Resetar histórico"):
    st.session_state.historico = []
    st.session_state.saldo = 1000.0

# Exibir histórico
if st.session_state.historico:
    df = pd.DataFrame(st.session_state.historico)
    df["Cor"] = df["numero"].apply(lambda x: "Verde" if x == 0 else "Vermelho" if x in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36] else "Preto")
    df["Par/Ímpar"] = df["numero"].apply(lambda x: "Zero" if x == 0 else "Par" if x % 2 == 0 else "Ímpar")
    df["Dúzia"] = df["numero"].apply(lambda x: "Zero" if x == 0 else "1ª" if x <= 12 else "2ª" if x <= 24 else "3ª")

    st.subheader("📊 Estatísticas")
    st.dataframe(df.tail(10))

    # 📈 Gráfico de frequência
    st.bar_chart(df["Cor"].value_counts())

    # 🧠 Alertas inteligentes
    ultimos = df["Cor"].tail(5).tolist()
    if len(set(ultimos)) == 1:
        st.warning(f"⚠️ Padrão detectado: {ultimos[0]} saiu 5 vezes seguidas!")

    # 📤 Exportar CSV
    csv = df.to_csv(index=False).encode()
    st.download_button("⬇️ Baixar CSV", csv, "historico_roleta.csv", "text/csv")

    # 💰 Simulação de aposta
    st.subheader("🎲 Aposta com saldo virtual")
    tipo = st.selectbox("Tipo", ["Cor", "Número"])
    valor = st.number_input("Valor da aposta", min_value=1.0, max_value=st.session_state.saldo)
    selecao = st.text_input("Escolha (ex: Vermelho ou número exato)")

    if st.button("💸 Apostar"):
        ultimo = df.iloc[-1]
        ganhou = False
        if tipo == "Cor" and selecao.lower() == ultimo["Cor"].lower():
            ganhou = True
            premio = valor * 2
        elif tipo == "Número" and int(selecao) == ultimo["numero"]:
            ganhou = True
            premio = valor * 36
        else:
            premio = 0

        st.session_state.saldo += premio - valor
        st.info(f"{'✅ Ganhou' if ganhou else '❌ Perdeu'} | Saldo: R$ {st.session_state.saldo:.2f}")

    st.success(f"💼 Saldo atual: R$ {st.session_state.saldo:.2f}")

else:
    st.warning("Adicione números para começar.")

# 📡 Placeholder scraping Evolution
with st.expander("🔍 Scraping Evolution (futuro)"):
    st.info("Aqui ficará a leitura automática da roleta Evolution via navegador.")
