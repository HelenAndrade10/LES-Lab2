import os
from graphqlclient import GraphQLClient
from datetime import datetime as date
import json
import csv
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

dadosArquivo = open('databases/repos_java.csv', 'w', newline='')

url = "https://api.github.com/graphql"
token = API_TOKEN
today = date.utcnow()
variables = {}

client = GraphQLClient(url)
client.inject_token(token=token)

end_cursor = 'null'
i = 1
writer = csv.writer(dadosArquivo)
header = [
    "Name",
    "URL",
    "Stargazers",
    "Created At",
    "Age", 
    "Language",
    "Releases",
]
writer.writerow(header)

endedFirstSearch = False
while i < 1050:
    starsFilter = ''
    if (not endedFirstSearch):
        starsFilter = '>1600'
    else:
        starsFilter = '1600..3042'
    query = """
            query {
              search(query: "is:public stars:""" + starsFilter + """ sort:stars language:java", type: REPOSITORY, first: 50, after: """ + end_cursor + """) {
                pageInfo{
                  hasNextPage
                  endCursor
                }
                nodes {
                  ... on Repository {
                    nameWithOwner
                    url
                    stargazerCount
                    createdAt
                    primaryLanguage { 
                      name 
                    }
                    releases { 
                      totalCount 
                    }
                  }
                }
              }
            }
            """
    
    try:
      data = json.loads(client.execute(query=query, variables=variables))
      results = data["data"]["search"]
    except:
      print("Falha! Tentando novamente...")
      continue
    
    
    hasNextPage = results["pageInfo"]["hasNextPage"]
    if (hasNextPage):
        end_cursor = '"' + results["pageInfo"]["endCursor"] + '"'
    else:
        endedFirstSearch = True

    variables["after"] = end_cursor
    repositories = results["nodes"]
    
    

    for repo in repositories:
        name = repo["nameWithOwner"]
        url = repo["url"]
        stargazers_count = repo["stargazerCount"]
        created_at = date.strptime(repo["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
        age = (today - created_at).days
        language = repo["primaryLanguage"]["name"] if repo["primaryLanguage"] is not None else "none"
        releases = repo["releases"]["totalCount"]

        print("Index: " + str(i))
        row = [
          name,
          url,
          stargazers_count,
          created_at,
          age,
          language,
          releases,
        ]
        writer.writerow(row)
        i = i + 1
    
    if endedFirstSearch:
        end_cursor = 'null'
        

print(15 * "-" + "FIM" + 15 * "-")

dadosArquivo.close()