import os
import subprocess
import pandas as pd
import shutil

def handle_remove_readonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise

def deletarDiretorio(diretorio):
    if os.path.exists(diretorio):
        print("Deletando diretório: '" + diretorio + "'\n")
        shutil.rmtree(diretorio, True)
    else:
        print("O diretório '" + diretorio + "' não existe.\n")
        
def descarta(descarte_df, repo_name):
    row = pd.Series({'nome_repo': repo_name})
    descarte_df.loc[len(descarte_df)] = row
    descarte_df.to_csv('databases/descarte.csv', index=False)

repos_dir = "repositorios"
if (not os.path.isdir(repos_dir)):
        os.mkdir(repos_dir)

repos_df = pd.read_csv('databases/repos_java.csv')
repos_url = repos_df['URL'].to_list()

for url in repos_url:
    repo_name = str(repos_df.loc[repos_df["URL"] == url, "Name"].values[0])
    repo_dir = repos_dir + '/' + repo_name.replace('/', '-')
    
    print('-' * 40)
    print("Repositório: " + repo_name)
    
    # carrega 'metricas.csv' 
    metricas_df = pd.read_csv('databases/metricas.csv')
    
    
    if (metricas_df[metricas_df.columns[0]].count() > 999):
        print("FIM")
        break
    
    # Verifica se o repo já foi minerado
    contem_repo_name = metricas_df['repo_nome'].str.contains(repo_name).any()
    if (contem_repo_name):
        print("repositório já minerado, pulando...\n\n")
        continue
    
    descarte_df = pd.read_csv('databases/descarte.csv')
    contem_repo_name = descarte_df['nome_repo'].str.contains(repo_name).any()
    if (contem_repo_name):
        print("repositório já descartado, pulando...\n\n")
        continue
    
    # clona o repositório
    cmd_clone = ['git', 'clone', url, repo_dir]
    subprocess.run(cmd_clone, shell=True)
    
    # executa o ck
    cmd_ck = ['java', '-jar', 'tools/ck-0.7.1.jar', repo_dir, 'false', '0', 'false' 'output']
    subprocess.run(cmd_ck, shell=True)

    # carrega o arquivo 'class.csv'
    class_df = None
    try:
        class_df = pd.read_csv('class.csv')
    except:
        print("Falha ao carregar 'class.csv', pulando...")
        descarta(descarte_df, repo_name)
        continue

    # valida as métricas coletadas no arquivo 'class.csv'
    if (class_df[class_df.columns[0]].count() == 0):
        deletarDiretorio(repo_dir)
        print('Repositório sem dados, pulando...\n\n')
        descarta(descarte_df, repo_name)
        continue
    
    # coleta métricas do arquivo 'class.csv'
    soma_loc = class_df['loc'].sum()
    mediana_cbo = class_df['cbo'].median()
    mediana_dit = class_df['dit'].median()
    mediana_lcom = class_df['lcom'].median()
    
    # inclui as métricas do repositório em 'metricas.csv'
    row = pd.Series({'repo_nome': repo_name, 'soma_loc': soma_loc, 'mediana_cbo': mediana_cbo, 'mediana_dit': mediana_dit, 'mediana_lcom': mediana_lcom})
    metricas_df.loc[len(metricas_df)] = row
    
    # escreve as métricas no csv
    metricas_df.to_csv('databases/metricas.csv', index=False)
    deletarDiretorio(repo_dir)
    print("Repositório minerado!\n\n")
    