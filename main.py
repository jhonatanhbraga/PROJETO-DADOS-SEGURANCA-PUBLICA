import streamlit as st
import pandas as pd
import pyodbc


# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Painel de Segurança Pública - RJ",
    page_icon="🚔",
    layout="wide"
)


# ==========================================
# CONEXÃO COM SQL SERVER
# ==========================================

dados_conexao = (
    "Driver=SQL Server;"
    "Server=JVAPRENDIZ;"
    "Database=SegurancaRJ;"
)

conexao = pyodbc.connect(dados_conexao)


# ==========================================
# TÍTULO
# ==========================================

st.title("🚔 Painel de Segurança Pública do RJ")

st.markdown(
    "Análise de ocorrências registradas por município, "
    "mês e CISP."
)

st.divider()


# ==========================================
# BUSCAR DADOS DO SQL SERVER
# ==========================================

comando = """
SELECT
    ano,
    munic,
    mes,
    cisp,
    roubo_rua,
    furto_celular,
    roubo_veiculo
FROM ocorrencias
"""

df = pd.read_sql(comando, conexao)


# ==========================================
# INDICADORES
# ==========================================

total_ocorrencias = len(df)

total_roubos_rua = df["roubo_rua"].sum()

total_furtos_celular = df["furto_celular"].sum()

total_roubos_veiculo = df["roubo_veiculo"].sum()


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Registros",
    f"{total_ocorrencias:,}".replace(",", ".")
)

col2.metric(
    "Roubos de rua",
    f"{total_roubos_rua:,}".replace(",", ".")
)

col3.metric(
    "Furtos de celular",
    f"{total_furtos_celular:,}".replace(",", ".")
)

col4.metric(
    "Roubos de veículo",
    f"{total_roubos_veiculo:,}".replace(",", ".")
)


st.divider()


# ==========================================
# FILTROS
# ==========================================

st.subheader("🔎 Filtros")

col1, col2, col3 = st.columns(3)


with col1:

    anos = sorted(df["ano"].unique())

    ano_selecionado = st.selectbox(
        "Ano",
        ["Todos"] + anos
    )


with col2:

    municipios = sorted(df["munic"].unique())

    municipio_selecionado = st.selectbox(
        "Município",
        ["Todos"] + municipios
    )


with col3:

    meses = sorted(df["mes"].unique())

    mes_selecionado = st.selectbox(
        "Mês",
        ["Todos"] + meses
    )


# ==========================================
# APLICAR FILTROS
# ==========================================

df_filtrado = df.copy()


if ano_selecionado != "Todos":

    df_filtrado = df_filtrado[
        df_filtrado["ano"] == ano_selecionado
    ]


if municipio_selecionado != "Todos":

    df_filtrado = df_filtrado[
        df_filtrado["munic"] == municipio_selecionado
    ]


if mes_selecionado != "Todos":

    df_filtrado = df_filtrado[
        df_filtrado["mes"] == mes_selecionado
    ]


# ==========================================
# GRÁFICOS
# ==========================================

st.subheader("📊 Ocorrências")


col1, col2 = st.columns(2)


with col1:

    roubos_por_ano = (
        df_filtrado
        .groupby("ano")["roubo_rua"]
        .sum()
    )

    st.line_chart(
        roubos_por_ano,
        x_label="Ano",
        y_label="Quantidade"
    )


with col2:

    furtos_por_ano = (
        df_filtrado
        .groupby("ano")["furto_celular"]
        .sum()
    )

    st.line_chart(
        furtos_por_ano,
        x_label="Ano",
        y_label="Quantidade"
    )


# ==========================================
# TABELA
# ==========================================

st.subheader("📋 Dados")

st.dataframe(
    df_filtrado,
    use_container_width=True,
    height=400
)


# ==========================================
# ENCERRAR CONEXÃO
# ==========================================

conexao.close()