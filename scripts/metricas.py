import os
import subprocess
import pandas as pd


repos_dir = "repositorios"
if (not os.path.isdir(repos_dir)):
        os.mkdir(repos_dir)

repos_df = pd.read_csv('databases/repos_java.csv')
repos_url = repos_df['URL'].to_list()

for url in repos_url:
    if url == 'https://github.com/Snailclimb/JavaGuide':
        continue
    print(url)

    repo_name = str(repos_df.loc[repos_df["URL"] == url, "Name"].values[0])
    repo_dir = repos_dir + '/' + repo_name.replace('/', '-')
    
    # clona o repositório
    cmd_clone = ['git', 'clone', url, repo_dir]
    subprocess.run(cmd_clone, shell=True)
    
    # executa o ck
    cmd_ck = ['java', '-jar', 'tools/ck-0.7.1.jar', repo_dir, 'false', '0', 'false' 'output']
    subprocess.run(cmd_ck, shell=True)
    
    # coleta métricas do arquivo 'class.csv'
    metrics_df = pd.read_csv('class.csv')

    
    soma_loc = metrics_df['loc'].sum()
    mediana_cbo = metrics_df['cbo'].median()
    mediana_dit = metrics_df['dit'].median()
    mediana_lcom = metrics_df['lcom'].median()

    # carrega 'metricas.csv' e inclui as métricas do repositório
    metricas_csv = pd.read_csv('databases/metricas.csv')
    
    row = pd.Series({'repo_nome': repo_name, 'soma_loc': soma_loc, 'mediana_cbo': mediana_cbo, 'mediana_dit': mediana_dit, 'mediana_lcom': mediana_lcom})
    metricas_csv.loc[len(metricas_csv)] = row
    
    # escreve os métricas no csv
    metricas_csv.to_csv('databases/metricas.csv', index=False)
    
    break
    