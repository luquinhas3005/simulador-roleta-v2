
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import base64
import io

st.set_page_config(page_title="Simulador Completo de Roleta", layout="centered")

st.title("🎰 Simulador Completo de Estratégias - Roleta Europeia")

# Inicialização de sessão
if "historico" not in st.session_state:
    st.session_state.historico = []
if "saldo" not in st.session_state:
    st.session_state.saldo = 1000.0

# Entrada do número
st.subheader("🔢 Inserção Manual")
numero = st.number_input("Número sorteado (0 a 36)", min_value=0, max_value=36, step=1)
if st.button("Adicionar número"):
    st.session_state.historico.append({"numero": numero, "data": datetime.datetime.now()})

# Reset
if st.button("🔄 Resetar tudo"):
    st.session_state.historico = []
    st.session_state.saldo = 1000.0

# Dados
if st.session_state.historico:
    df = pd.DataFrame(st.session_state.historico)
    df["Cor"] = df["numero"].apply(lambda x: "Verde" if x == 0 else "Vermelho" if x in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36] else "Preto")
    df["Par/Ímpar"] = df["numero"].apply(lambda x: "Zero" if x == 0 else "Par" if x % 2 == 0 else "Ímpar")
    df["Alto/Baixo"] = df["numero"].apply(lambda x: "Zero" if x == 0 else "Alto (19-36)" if x > 18 else "Baixo (1-18)")
    df["Dúzia"] = df["numero"].apply(lambda x: "Zero" if x == 0 else "1ª (1-12)" if x <= 12 else "2ª (13-24)" if x <= 24 else "3ª (25-36)")
    df["Coluna"] = df["numero"].apply(lambda x: "Zero" if x == 0 else f"Coluna {(x-1)%3+1}")

    st.subheader("📊 Estatísticas")
    st.dataframe(df.tail(10))

    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(df["Cor"].value_counts())
    with col2:
        st.bar_chart(df["Par/Ímpar"].value_counts())

    st.bar_chart(df["Dúzia"].value_counts())

    # Exportar
    csv = df.to_csv(index=False).encode()
    b64 = base64.b64encode(csv).decode()
    st.download_button("⬇️ Baixar histórico CSV", csv, "historico_roleta.csv", "text/csv")

    # Simulação de aposta
    st.subheader("🎲 Simulação de Apostas")
    tipo_aposta = st.selectbox("Tipo", ["Cor", "Par/Ímpar", "Dúzia", "Número"])
    valor_aposta = st.number_input("Valor da Aposta", min_value=1.0, max_value=st.session_state.saldo, value=10.0)
    selecao = None

    if tipo_aposta == "Cor":
        selecao = st.selectbox("Escolha", ["Vermelho", "Preto"])
    elif tipo_aposta == "Par/Ímpar":
        selecao = st.selectbox("Escolha", ["Par", "Ímpar"])
    elif tipo_aposta == "Dúzia":
        selecao = st.selectbox("Escolha", ["1ª (1-12)", "2ª (13-24)", "3ª (25-36)"])
    elif tipo_aposta == "Número":
        selecao = st.number_input("Número exato", 0, 36)

    if st.button("💰 Apostar"):
        if tipo_aposta == "Cor":
            ganhou = df["Cor"].iloc[-1] == selecao
            ganho = valor_aposta * 2 if ganhou else 0
        elif tipo_aposta == "Par/Ímpar":
            ganhou = df["Par/Ímpar"].iloc[-1] == selecao
            ganho = valor_aposta * 2 if ganhou else 0
        elif tipo_aposta == "Dúzia":
            ganhou = df["Dúzia"].iloc[-1] == selecao
            ganho = valor_aposta * 3 if ganhou else 0
        elif tipo_aposta == "Número":
            ganhou = df["numero"].iloc[-1] == selecao
            ganho = valor_aposta * 36 if ganhou else 0

        st.session_state.saldo += ganho - valor_aposta
        st.success(f"{'✅ Ganhou' if ganhou else '❌ Perdeu'} | Novo saldo: R$ {st.session_state.saldo:.2f}")

    st.info(f"💵 Saldo atual: R$ {st.session_state.saldo:.2f}")
else:
    st.warning("Nenhum número inserido ainda.")
