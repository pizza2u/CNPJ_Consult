import requests

url = "https://publica.cnpj.ws/cnpj/27865757000102"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Erro na requisição: {response.status_code}")
