import pyodbc
import pandas as pd

dados_conexao = (
    "Driver=SQL Server;"
    "Server=JVAPRENDIZ;"
    "Database=SegurancaRJ;"
)

conexao = pyodbc.connect(dados_conexao)

print("Conexao bem sucedida!")

df = pd.read_csv(
    "dados/BaseDPEvolucaoMensalCisp.csv",
    sep=";",
    encoding="latin1"
)

print(df.columns.tolist())

df = df[
    [
    "ano",
    "munic",
    "mes",
    "cisp",
    "roubo_rua",
    "furto_celular",
    "roubo_veiculo",
    ]    
]

print("\n--- PRIMEIRAS LINHAS ---")
print(df.head())

print("\n--- INFORMAÇÕES DA BASE ---")
print(df.info())

print("\n--- VALORES VAZIOS ---")
print(df.isnull().sum())

print("\n--- QUANTIDADE DE LINHAS E COLUNAS ---")
print(df.shape)

print("\n--- DUPLICADOS ---")
print(df.duplicated().sum())

cursor = conexao.cursor()

dados = df.values.tolist()

cursor.executemany(
    """
    INSERT INTO ocorrencias
    (
        ano,
        munic,
        mes,
        cisp,
        roubo_rua,
        furto_celular,
        roubo_veiculo
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    dados
)

conexao.commit()

print("Dados inseridos com sucesso!")

cursor.close()
conexao.close()









