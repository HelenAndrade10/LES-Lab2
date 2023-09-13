# LES - Lab 2

## 1. Seleção de Repositórios
Com o objetivo de analisar repositórios relevantes, escritos na linguagem estudada, coletaremos os top-1.000 repositórios Java mais populares do GitHub, calculando cada uma das métricas definidas na Seção 3.

 

### 2. Questões de Pesquisa
Desta forma, este laboratório tem o objetivo de responder às seguintes questões de pesquisa:

1. RQ 01. Qual a relação entre a popularidade dos repositórios e as suas características de qualidade?
2. RQ 02. Qual a relação entre a maturidade do repositórios e as suas características de qualidade ? 
3. RQ 03. Qual a relação entre a atividade dos repositórios e as suas características de qualidade?  
4. RQ 04. Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?  
 

### 3. Definição de Métricas
Para cada questão de pesquisa, realizaremos a comparação entre as características do processo de desenvolvimento dos repositórios e os valores obtidos para as métricas definidas nesta seção. Para as métricas de processo, define-se:

- Popularidade: número de estrelas
- Tamanho: linhas de código (LOC) e linhas de comentários
- Atividade: número de releases
- Maturidade: idade (em anos) de cada repositório coletado

Por métricas de qualidade, entende-se:

- CBO: Coupling between objects
- DIT: Depth Inheritance Tree
- LCOM: Lack of Cohesion of Methods
 

### 4. Coleta e Análise de Dados
Para análise das métricas de popularidade, atividade e maturidade, serão coletadas informações dos repositórios mais populares em Java, utilizando as APIs REST ou GraphQL do GitHub. Para medição dos valores de qualidade, utilizaremos uma ferramenta de análise estática de código (por exemplo, o CKLinks to an external site.).

Importante: a ferramenta CK gera diferentes arquivos .csv com os resultados para níveis de análise diferentes. É importante que você sumarize os dados obtidos. 