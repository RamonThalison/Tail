import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.cluster import KMeans

# Carregando o dataset
movies = pd.read_csv('https://raw.githubusercontent.com/TailUFPB/processo2fase/master/2024.2/data/top1000_tmdb.csv')

# Limpeza e preparação dos dados
movies = movies.dropna()  # Remove linhas com valores nulos
movies = movies.drop(columns=['id', 'title', 'overview', 'tagline', 'original_title'])  # Remove colunas irrelevantes

# Codificação de variáveis categóricas
categorical_columns = ['status', 'original_language', 'genres', 'production_companies', 'production_countries', 'spoken_languages', 'keywords']
movies = pd.get_dummies(movies, columns=categorical_columns, drop_first=True)

# Seleção de colunas numéricas para análise
numerical_columns = ['budget', 'revenue', 'runtime', 'vote_count']
X = movies[numerical_columns]  # Atribui apenas as colunas numéricas a X
y = movies['vote_average']  # Atribui a coluna alvo (nota média) a y

# Padronização dos dados numéricos
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Divisão dos dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Comparação de modelos de regressão
models = {
    "Regressão Linear": LinearRegression(),
    "Árvore de Decisão": DecisionTreeRegressor(random_state=42)
}

print("\n----- Aprendizado Supervisionado -----")
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Modelo: {name}")
    print(f"Erro Quadrático Médio (MSE): {mse:.2f}")
    print(f"Coeficiente de Determinação (R²): {r2:.2f}\n")

# Clustering (aprendizado não supervisionado)
clustering_features = movies[['vote_average', 'vote_count', 'budget', 'revenue', 'runtime']]

# Encontrando o número ideal de clusters
inertia = []
k_values = range(1, 11)
for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(clustering_features)
    inertia.append(kmeans.inertia_)

# Plotando o método do cotovelo
plt.figure(figsize=(8, 5))
plt.plot(k_values, inertia, marker='o')
plt.title("Método do Cotovelo")
plt.xlabel("Número de Clusters (k)")
plt.ylabel("Inércia")
plt.show()

# Escolha do número de clusters e criação dos clusters
optimal_k = 4  # Escolhido visualmente pelo método do cotovelo
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
movies['cluster'] = kmeans.fit_predict(clustering_features)

# Análise dos clusters
print("\n----- Aprendizado Não-Supervisionado -----")
for i in range(optimal_k):
    cluster_movies = movies[movies['cluster'] == i]
    print(f"\nCluster {i}:")
    print(cluster_movies[['vote_average', 'vote_count']].describe())

print("\nDistribuição de clusters:")
print(movies['cluster'].value_counts())