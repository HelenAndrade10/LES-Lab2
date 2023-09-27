import pandas as pd

# Lê os arquivos CSV em DataFrames
repos_java_df = pd.read_csv('databases/repos_java.csv')
metricas_df = pd.read_csv('databases/metricas.csv')

# Renomeia a coluna 'repo_nome' para 'Name' no segundo DataFrame para facilitar a junção
metricas_df = metricas_df.rename(columns={'soma_loc': 'LOC'})
metricas_df = metricas_df.rename(columns={'mediana_cbo': 'CBO'})
metricas_df = metricas_df.rename(columns={'mediana_dit': 'DIT'})
metricas_df = metricas_df.rename(columns={'mediana_lcom': 'LCOM'})
metricas_df = metricas_df.rename(columns={'repo_nome': 'Name'})

# Realiza a junção dos DataFrames usando a coluna 'Name'
result_df = repos_java_df.merge(metricas_df, on='Name', how='inner')

# Exibe o DataFrame resultante
print(result_df)

# Salva o DataFrame resultante em um novo arquivo CSV, se desejar
result_df.to_csv('databases/resultado.csv', index=False)

