import pandas as pd
from pathlib import Path
import subprocess
import os

REPO = Path(__file__).parent
UPLOAD = REPO / "upload"
ARQUIVO = UPLOAD / "MARIANA.xlsx"

if not ARQUIVO.exists():
    raise FileNotFoundError(f"Arquivo não encontrado: {ARQUIVO}")

abas = pd.read_excel(
    ARQUIVO,
    sheet_name=None,
    header=1
)

print("Abas encontradas:")
print(list(abas.keys()))

arquivos_gerados = 0

for aba in abas:

    df = abas[aba]

    # remove primeira coluna
    df = df.iloc[:, 1:]

    # remove linhas vazias
    df = df.dropna(how="all")

    nome_saida = aba.strip().lower() + ".xlsx"

    df.to_excel(
        UPLOAD / nome_saida,
        index=False
    )

    print(f"Gerado: {nome_saida}")
    arquivos_gerados += 1

if arquivos_gerados > 0:

    os.remove(ARQUIVO)

    subprocess.run(["git", "add", "upload"], cwd=REPO)

    subprocess.run(
        ["git", "commit", "-m", "Atualização automática portal mariana"],
        cwd=REPO
    )

    subprocess.run(["git", "push"], cwd=REPO)

    print("Concluído.")
else:
    print("Nenhum arquivo gerado.")