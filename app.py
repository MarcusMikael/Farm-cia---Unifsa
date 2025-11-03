import streamlit as st
import pandas as pd
from datetime import datetime, time
import os

# Logo UNIFSA
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    st.image("unifsa.png", width=180)

st.divider()

# Configuração da página
st.set_page_config(page_title="Estágio Farmácia - UNIFSA", layout="wide")
with col2:
    st.title("Sistema de Controle de Estágio : Farmácia Escola" )

# Criar arquivos se não existirem
if not os.path.exists("frequencia.csv"):
    pd.DataFrame(columns=["Nome", "Data", "Entrada", "Saída", "Horas", "Assinatura Estagiário", "Assinatura Supervisor"]).to_csv("frequencia.csv", index=False)

if not os.path.exists("diario.csv"):
    pd.DataFrame(columns=["Nome", "Data", "Atividade", "Assinatura Supervisor"]).to_csv("diario.csv", index=False)

# Dividir em abas
abaFrequencia, abaDiario = st.tabs([" Controle de Frequência", " Diário de Campo"])

# =================== ABA Frequencia =====================
with abaFrequencia:
    st.subheader("Registro de Frequência")

    with st.form("form_frequencia"):
        nome = st.text_input("Nome do Estagiário")
        data = st.date_input("Data", datetime.today())
        entrada = st.time_input("Horário de Entrada", time(7, 0))
        saida = st.time_input("Horário de Saída", time(13, 0))
        horas = st.number_input("Frequência Acumulada (horas)", min_value=0.0, step=0.5)
        assinatura_estudante = st.text_input("Assinatura (Estagiário) !!Teste!!")
        assinatura_supervisor = st.text_input("Assinatura (Supervisor) !!Teste!!")
        enviar = st.form_submit_button("Salvar Registro")

        if enviar:
            df = pd.read_csv("frequencia.csv")
            novo = pd.DataFrame([[nome, data, entrada, saida, horas, assinatura_estudante, assinatura_supervisor]],
                                columns=df.columns)
            df = pd.concat([df, novo], ignore_index=True)
            df.to_csv("frequencia.csv", index=False)
            st.success("Registro salvo com sucesso!")

    st.divider()
    st.subheader(" Registros de Frequência")
    df = pd.read_csv("frequencia.csv")
    st.dataframe(df)
# Soma o total de horas
    if not df.empty:
        total_horas = df["Horas"].sum()
        st.metric("⏱ Total de Horas Registradas", f"{total_horas} h")

# =================== ABA Diario =====================
with abaDiario:
    st.subheader("Registro do Diário de Campo")

    with st.form("form_diario"):
        nome2 = st.text_input("Nome do Estagiário", key="nome2")
        data2 = st.date_input("Data", datetime.today(), key="data2")
        atividade = st.text_area("Atividade Desenvolvida")
        assinatura_sup2 = st.text_input("Assinatura Digital (Supervisor)", key="sup2")
        enviar2 = st.form_submit_button("Salvar Registro")

        if enviar2:
            df2 = pd.read_csv("diario.csv")
            novo2 = pd.DataFrame([[nome2, data2, atividade, assinatura_sup2]],
                                 columns=df2.columns)
            df2 = pd.concat([df2, novo2], ignore_index=True)
            df2.to_csv("diario.csv", index=False)
            st.success(" Registro salvo com sucesso!")

    st.divider()
    st.subheader(" Registros do Diário de Campo")
    df2 = pd.read_csv("diario.csv")
    st.dataframe(df2)
