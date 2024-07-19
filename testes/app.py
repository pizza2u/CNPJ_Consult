import requests
import csv

def obter_dados_cnpj(cnpj):
    url = f"https://publica.cnpj.ws/cnpj/{cnpj}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao obter dados: {e}")
        return None

def salvar_em_csv(dados, arquivo):
    try:
        with open(arquivo, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Verifica se o arquivo está vazio para escrever o cabeçalho
                writer.writerow([
                    'CNPJ', 'Razão Social', 'Capital Social', 'Porte', 
                    'Natureza Jurídica', 'Atividade Principal', 'Município', 'UF'
                ])
            
            for item in dados:
                est = item.get('estabelecimento', {})
                writer.writerow([
                    item.get('cnpj', ''),
                    item.get('razao_social', ''),
                    item.get('capital_social', ''),
                    item.get('porte', {}).get('descricao', ''),
                    item.get('natureza_juridica', {}).get('descricao', ''),
                    est.get('atividade_principal', {}).get('descricao', ''),
                    est.get('cidade', {}).get('nome', ''),
                    est.get('estado', {}).get('sigla', '')
                ])
    except Exception as e:
        print(f"Erro ao salvar dados no CSV: {e}")

def menu():
    arquivo_csv = 'dados_cnpj.csv'
    while True:
        print("\nMenu")
        print("1. Inserir CNPJ")
        print("2. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cnpj = input("Digite o CNPJ (somente números): ")
            dados = obter_dados_cnpj(cnpj)
            if dados:
                salvar_em_csv([dados], arquivo_csv)
                print("Dados salvos com sucesso!")
            else:
                print("Não foi possível obter os dados do CNPJ.")
        elif opcao == '2':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
