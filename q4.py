import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

dataset = pd.read_csv('https://raw.githubusercontent.com/tmfilho/akcdata/master/data/akc-data-latest.csv', sep = ',')
dataset.head()

# Selecionar apenas colunas numéricas
dataset_numerico = dataset.select_dtypes(include=['float64', 'int64'])

medias = dataset_numerico.mean() # Medidas de Localização
medianas = dataset_numerico.median()

variancia = dataset_numerico.var()
desvio_padrao = dataset_numerico.std() # Medidas de Dispersão
IQR = dataset_numerico.quantile(0.75) - dataset_numerico.quantile(0.25)

valores_unicos = dataset_numerico.nunique() # Valores Únicos

plt.figure(figsize=(15, 10))
dataset_numerico.boxplot() # Boxplot para cada coluna numérica
plt.title('Boxplots das Colunas Numéricas')
plt.xticks(rotation=90)


print('Medidas de Localização:')
print(f'Médias:\n{medias}')
print(f'Medianas:\n{medianas}')
print(f'\nMedidas de Dispersão:') # Exibir Medidas de Localização e Dispersão
print(f'Variância:\n{variancia}')
print(f'Desvio Padrão: {desvio_padrao}')
print(f'Intervalo Interquartil (IQR):\n{IQR}')


print('\nValores Únicos por Coluna:') # Exibir Valores Únicos por Coluna
print(valores_unicos)
plt.show()

dataset_limpo = dataset.dropna() # Identificar e tratar valores ausentes
duplicatas = dataset_limpo.duplicated() # Identificar e remover duplicatas
dataset_limpo = dataset_limpo.drop_duplicates()
dataset_limpo['popularity'] = pd.to_numeric(dataset_limpo['popularity'], errors='coerce')
#transformei a coluna popularity em numerico
dataset_limpo.drop(['description', 'temperament'], axis=1, inplace=True)
# description e temprament eram dados muito grandes(e não númericos) pouco relevantes
print(dataset_limpo.dtypes)

dataset_limpo['height_energy_ratio'] = ((dataset_limpo['min_height'] + dataset_limpo['max_height'])/2)/dataset_limpo['energy_level_value']
# faz uma relação da média do tamanho com a energia das raças
print(dataset_limpo['height_energy_ratio']) #verifica se a coluna foi criada

label_encoder = LabelEncoder()
for column in dataset_limpo.columns: # transformando colunas não númericas em inteiros
  if dataset_limpo[column].dtype == object:
    dataset_limpo[column] = label_encoder.fit_transform(dataset_limpo[column])
print(dataset_limpo.dtypes) # verificando os tipos dos dados

