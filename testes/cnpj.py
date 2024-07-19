import requests
import csv

url = "https://publica.cnpj.ws/cnpj/27865757000102"


resp = requests.get(url)

if resp.status_code == 200:
    data = resp.json()

    # Extraindo informações relevantes
    cnpj = data.get('cnpj', 'N/A')
    razao_social = data.get('razao_social', 'N/A')
    nome_fantasia = data.get('nome_fantasia', 'N/A')
    natureza_juridica = data.get('natureza_juridica', {}).get('descricao', 'N/A')
    municipio = data.get('estabelecimento', {}).get('municipio', {}).get('nome', 'N/A')
    uf = data.get('estabelecimento', {}).get('estado', {}).get('sigla', 'N/A')

    # Definindo cabeçalhos e dados para o CSV
    headers = ['CNPJ', 'Razão Social', 'Nome Fantasia', 'Natureza Jurídica', 'Município', 'UF']
    rows = [[cnpj, razao_social, nome_fantasia, natureza_juridica, municipio, uf]]

    # Escrevendo os dados em um arquivo CSV
    with open('dados_cnpj.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

    print("Dados salvos em 'dados_cnpj.csv'")
else:
    print(f"Erro na requisição: {resp.status_code}")
