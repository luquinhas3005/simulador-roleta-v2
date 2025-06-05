
import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador de Roleta", layout="centered")

st.title("🎰 Simulador de Roleta")

# Inicializando estado da sessão
if "historico" not in st.session_state:
    st.session_state.historico = []
if "saldo" not in st.session_state:
    st.session_state.saldo = 1000
if "resultados" not in st.session_state:
    st.session_state.resultados = []

# Função de sorteio
def girar_roleta():
    return random.randint(0, 36)

# Interface de apostas
col1, col2 = st.columns(2)
with col1:
    aposta_tipo = st.selectbox("Tipo de aposta", ["Número direto", "Vermelho", "Preto", "Ímpar", "Par", "1-18", "19-36"])
with col2:
    valor_aposta = st.number_input("Valor da aposta", min_value=1, max_value=st.session_state.saldo, value=10)

numero_escolhido = None
if aposta_tipo == "Número direto":
    numero_escolhido = st.number_input("Escolha um número (0–36)", min_value=0, max_value=36, value=7)

if st.button("🎲 Girar Roleta"):
    resultado = girar_roleta()
    ganho = 0
    ganhou = False

    # Lógica de vitória
    if aposta_tipo == "Número direto":
        if resultado == numero_escolhido:
            ganho = valor_aposta * 35
            ganhou = True
    elif aposta_tipo == "Vermelho":
        if resultado in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]:
            ganho = valor_aposta * 2
            ganhou = True
    elif aposta_tipo == "Preto":
        if resultado in [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]:
            ganho = valor_aposta * 2
            ganhou = True
    elif aposta_tipo == "Ímpar":
        if resultado != 0 and resultado % 2 == 1:
            ganho = valor_aposta * 2
            ganhou = True
    elif aposta_tipo == "Par":
        if resultado != 0 and resultado % 2 == 0:
            ganho = valor_aposta * 2
            ganhou = True
    elif aposta_tipo == "1-18":
        if 1 <= resultado <= 18:
            ganho = valor_aposta * 2
            ganhou = True
    elif aposta_tipo == "19-36":
        if 19 <= resultado <= 36:
            ganho = valor_aposta * 2
            ganhou = True

    st.session_state.saldo -= valor_aposta
    st.session_state.saldo += ganho

    # Registrar resultado
    st.session_state.historico.append({
        "Aposta": aposta_tipo if numero_escolhido is None else f"{aposta_tipo} ({numero_escolhido})",
        "Resultado": resultado,
        "Ganhou": "✅" if ganhou else "❌",
        "Ganho": ganho,
        "Saldo": st.session_state.saldo
    })
    st.session_state.resultados.append(resultado)

# Mostrar estatísticas
st.subheader("📊 Estatísticas")
total_jogos = len(st.session_state.historico)
total_apostado = total_jogos * valor_aposta if total_jogos > 0 else 0
total_ganho = sum([item["Ganho"] for item in st.session_state.historico])
roi = ((total_ganho - total_apostado) / total_apostado * 100) if total_apostado > 0 else 0

st.markdown(f"""
- **Total de rodadas:** {total_jogos}
- **Total apostado:** R$ {total_apostado}
- **Total ganho:** R$ {total_ganho}
- **Saldo atual:** R$ {st.session_state.saldo}
- **ROI:** {roi:.2f}%
""")

# Gráficos
if st.session_state.resultados:
    st.subheader("📈 Gráfico de saldo")
    df = pd.DataFrame(st.session_state.historico)
    fig, ax = plt.subplots()
    ax.plot(df["Saldo"], marker="o", linestyle="--")
    ax.set_title("Evolução do saldo")
    st.pyplot(fig)

    st.subheader("📉 Frequência dos números")
    freq = pd.Series(st.session_state.resultados).value_counts().sort_index()
    st.bar_chart(freq)

# Tabela de histórico
if st.session_state.historico:
    st.subheader("📋 Histórico de rodadas")
    st.dataframe(pd.DataFrame(st.session_state.historico))

# Botão de reset
if st.button("🔄 Resetar tudo"):
    st.session_state.clear()
    st.experimental_rerun()
