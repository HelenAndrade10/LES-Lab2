import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('databases/resultado.csv')


x_axis = ['Stargazers', 'Age', 'Releases', 'LOC']
y_axis = ['DIT', 'CBO', 'LCOM']

for x in x_axis:
    for y in y_axis:
        print('Relação', x, y)
        sns.pairplot(data=df, y_vars=y, x_vars=x, kind="reg", height=10)
        plt.show()
  