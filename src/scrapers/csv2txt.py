# Importando bibliotecas
import os
import pandas as pd

# Definindo diretório em que se encontram os arquivos csv
path = r'../data'

# Entrando no diretório e listando só os arquivos csv
os.chdir(path)
files = [f for f in os.listdir(path) if f.endswith('.csv')]

# Lendo cada arquivo .csv e salvando os textos da coluna 'texto' em um arquivo .txt
for file in files:
    df = pd.read_csv(file)
    with open(file[:-4] + '.txt', 'w', encoding='utf-8') as f:
        for texto in df['texto']:
            f.write(texto + '\n')