import requests
import json
import csv

url = "https://publica.cnpj.ws/suframa"

payload = json.dumps({
  "cnpj": "61940292006682",
  "inscricao": "210140267"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

if response.status_code == 200:
    data = response.json()

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
    with open('cnpj.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

    print("Dados salvos em 'cnpj.csv'")
else:
    print(f"Erro na requisição: {response.status_code}")
