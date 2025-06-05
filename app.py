
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador de Roleta Europeia - Evolution", layout="centered")

st.title("🎰 Simulador de Roleta Europeia - Evolution Gaming")

st.markdown("Insira os números sorteados manualmente conforme saem na roleta ao vivo.")

# Sessão de histórico
if "resultados" not in st.session_state:
    st.session_state.resultados = []

# Entrada manual
novo_resultado = st.number_input("Digite o número sorteado (0 a 36)", min_value=0, max_value=36, step=1)

if st.button("Adicionar"):
    st.session_state.resultados.append(novo_resultado)

if st.button("Resetar Histórico"):
    st.session_state.resultados = []

# Análise
if st.session_state.resultados:
    df = pd.DataFrame(st.session_state.resultados, columns=["Número"])
    df["Cor"] = df["Número"].apply(lambda x: "Verde" if x == 0 else "Vermelho" if x in [
        1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36] else "Preto")
    df["Par/Ímpar"] = df["Número"].apply(lambda x: "Zero" if x == 0 else "Par" if x % 2 == 0 else "Ímpar")
    df["Alto/Baixo"] = df["Número"].apply(lambda x: "Zero" if x == 0 else "Alto (19-36)" if x > 18 else "Baixo (1-18)")
    df["Dúzia"] = df["Número"].apply(lambda x: "Zero" if x == 0 else 
                                     "1ª (1-12)" if x <= 12 else 
                                     "2ª (13-24)" if x <= 24 else 
                                     "3ª (25-36)")

    st.subheader("📊 Estatísticas Gerais")
    st.write(df.tail(10))

    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(df["Número"].value_counts().sort_index())
    with col2:
        st.bar_chart(df["Cor"].value_counts())

    col3, col4 = st.columns(2)
    with col3:
        st.bar_chart(df["Par/Ímpar"].value_counts())
    with col4:
        st.bar_chart(df["Alto/Baixo"].value_counts())

    st.subheader("📈 Dúzias")
    st.bar_chart(df["Dúzia"].value_counts())

else:
    st.info("Insira pelo menos um número para começar a análise.")
