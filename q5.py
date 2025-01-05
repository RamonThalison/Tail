import pandas as pd
import matplotlib.pyplot as plt
import re
import nltk
from unidecode import unidecode
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

url = "https://raw.githubusercontent.com/TailUFPB/processo2fase/master/2024.2/data/games_sentiments.csv"
df = pd.read_csv(url)
print(df.head())

df = df.dropna() # limpando valores vazios
df = df.drop(columns='reviews_en') # já tem uma coluna com as mesmas coisas

def clean_text(text):
    text = unidecode(text)  # Substitui letras acentuadas por suas versões sem acento
    text = re.sub(r'[^\w\s]', '', text)  # Remove pontuação
    text = text.lower()  # Converte para letras minúsculas
    return text

# Aplicar a função de limpeza nas colunas 'reviews' e 'app_name'
df['reviews'] = df['reviews'].apply(clean_text)
df['app_name'] = df['app_name'].apply(clean_text)
df['time'] = pd.to_datetime(df['time'], dayfirst=True) # transformando numa coluna tipo data

print(df.head())

# tokenizando
df['reviews'] = df['reviews'].apply(word_tokenize)
df['app_name'] = df['app_name'].apply(word_tokenize)
print(df[['reviews', 'app_name']])

vazias = nltk.corpus.stopwords.words('portuguese')

# Função para remover stop words
def remove_stop_words(tokens, stop_words):
    return [word for word in tokens if word not in stop_words]

# Aplicando a função de remoção de stop words às colunas tokenizadas
df['reviews'] = df['reviews'].apply(lambda tokens: remove_stop_words(tokens, vazias))
df['app_name'] = df['app_name'].apply(lambda tokens: remove_stop_words(tokens, vazias))

print(df[['reviews', 'app_name']])

# Inicializando o lematizador
lemmatizer = WordNetLemmatizer()

# Função para lematizar tokens
def lemmatize_tokens(tokens):
    return [lemmatizer.lemmatize(word) for word in tokens]

# Aplicar a lematização as colunas
df['reviews'] = df['reviews'].apply(lemmatize_tokens)
df['app_name'] = df['app_name'].apply(lemmatize_tokens)

print(df)

# pegando os valores da coluna
classification_counts = df['classification'].value_counts()
# Visualizando a distribuição das classes
plt.figure(figsize=(8, 6))
classification_counts.plot(kind='bar', color=['#1f77b4', '#ff7f0e', '#2ca02c'])
plt.title('Distribuição das Classes de Sentimento')
plt.xlabel('Classe de Sentimento')
plt.ylabel('Número de Exemplos')
plt.xticks(ticks=[0, 1, 2], labels=['Negativo (-1)', 'Neutro ou incapaz de classificar (0)', 'Positivo (1)'], rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Contando as palavras por classificação
def maisComuns(df, class_label, top_n=10):
    # Filtrando os dados pela classificação
    subset = df[df['classification'] == class_label]
    # Concatenando todas as listas de tokens em uma única lista
    palavras = [word for tokens in subset['reviews'] for word in tokens]
    word_counts = Counter(palavras)
    # Obtendo as palavras mais comuns
    return word_counts.most_common(top_n)

# Palavras mais frequentes por classificação
palavrasPositivas = maisComuns(df, 1)
palavrasNeutras = maisComuns(df, 0)
palavrasNegativas = maisComuns(df, -1)

# Função para plotar palavras mais frequentes
def mostrarMaisComuns(word_counts, title):
    words, counts = zip(*word_counts)
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='skyblue')
    plt.title(title)
    plt.xlabel('Palavras')
    plt.ylabel('Frequência')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# Plotando palavras mais frequentes para cada classe
mostrarMaisComuns(palavrasPositivas, 'Palavras Mais Frequentes - Sentimento Positivo')
mostrarMaisComuns(palavrasNeutras, 'Palavras Mais Frequentes - Sentimento Neutro')
mostrarMaisComuns(palavrasNegativas, 'Palavras Mais Frequentes - Sentimento Negativo')

# Função para plotar comparação entre palavras positivas e negativas
def plot_word_comparison(pos_words, neg_words, top_n=10):
    pos_dict = dict(pos_words)
    neg_dict = dict(neg_words)

    common_words = set(pos_dict.keys()).intersection(set(neg_dict.keys()))

    pos_values = [pos_dict[word] for word in common_words]
    neg_values = [neg_dict[word] for word in common_words]

    x = range(len(common_words))

    plt.figure(figsize=(14, 7))
    plt.bar(x, pos_values, width=0.4, label='Positivo', color='skyblue', align='center')
    plt.bar(x, neg_values, width=0.4, label='Negativo', color='salmon', align='edge')
    plt.xlabel('Palavras')
    plt.ylabel('Frequência')
    plt.title('Comparação das Palavras Mais Frequentes entre Textos Positivos e Negativos')
    plt.xticks(x, list(common_words), rotation=45, ha='right')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# Plotando comparação entre palavras mais frequentes
plot_word_comparison(palavrasPositivas, palavrasNegativas)

# Filtrando as linhas com classificação positiva (1) e score < 3
divergent_positive = df[(df['classification'] == 1) & (df['score'] < 3)]

# Filtrando as linhas com classificação negativa (-1) e score > 3
divergent_negative = df[(df['classification'] == -1) & (df['score'] > 3)]

# Exibindo as divergências
print("Divergências de classificação positiva com score < 3:")
print(divergent_positive)

print("\nDivergências de classificação negativa com score > 3:")
print(divergent_negative)