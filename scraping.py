# importe a biblioteca usada para consultar uma URL
import urllib.request
import pandas as pd

# importe as funções BeautifulSoup para analisar os dados retornados do site
from bs4 import BeautifulSoup

# especifique o URL
inea = "http://alertadecheias.inea.rj.gov.br/dados/piabanha.php"

# Consulte o site e retorne o html para a variável 'page'
page = urllib.request.urlopen(inea)

# Parse o html na variável 'page' e armazene-o no formato BeautifulSoup
soup = BeautifulSoup(page, "html.parser")


table = soup.find('table', attrs={'class': 'TF'})

a = []
b = []
c = []
d = []
e = []
f = []


for row in table.findAll("tr"):  # para tudo que estiver em <tr>
    cells = row.findAll('td')  # variável para encontrar <td>
    if len(cells) == 17:  # número de colunas
        a.append(cells[0].find(string=True))  # iterando sobre cada linha
        b.append(cells[1].find('a').string)
        c.append(cells[2].find(string=True))
        d.append(cells[3].find('img'))
        e.append(cells[4].find(string=True))
        f.append(cells[5].find(string=True))


df = pd.DataFrame()

df['Municipio'] = a
df['Curso da Água'] = b
df['Nome da Estação'] = c
df['Status do Rio'] = d
df['Última Leitura'] = e
df['Status Monitoramento'] = f

print(df)
