import requests
import csv

def obter_dados_cnpj(cnpj):
    url = f"https://publica.cnpj.ws/cnpj/{cnpj}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        dados = response.json()
        print(dados)  # Adicione esta linha para verificar o JSON
        return dados
    except requests.RequestException as e:
        print(f"Erro ao obter dados: {e}")
        return None

def determinar_natureza_tipo(dados):
    """Função para determinar o tipo de natureza jurídica com base na descrição."""
    natureza_juridica = dados.get('natureza_juridica', {}).get('descricao', '')
    
    if 'municipal' in natureza_juridica.lower():
        return 'Municipal'
    elif 'estadual' in natureza_juridica.lower():
        return 'Estadual'
    elif 'federal' in natureza_juridica.lower():
        return 'Federal'
    else:
        return 'Não Especificado'

def determinar_tipo(dados):
    """Função para determinar se é Filial ou Matriz. Ajuste conforme necessário."""
    tipo = dados.get('tipo', '')
    if tipo.lower() == 'matriz':
        return 'Matriz'
    elif tipo.lower() == 'filial':
        return 'Filial'
    else:
        return 'Não Especificado'

def salvar_em_csv(cnpj, dados, arquivo):
    try:
        with open(arquivo, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Verifica se o arquivo está vazio para escrever o cabeçalho
                writer.writerow([
                    'CNPJ', 'Razão Social', 'Capital Social', 'Porte', 
                    'Natureza Jurídica', 'Natureza Tipo', 'Tipo', 'Atividade Principal', 'Município', 'UF'
                ])
            
            est = dados.get('estabelecimento', {})
            cidade = est.get('cidade', {})
            estado = est.get('estado', {})
            writer.writerow([
                cnpj,  # Adiciona o CNPJ digitado pelo usuário
                dados.get('razao_social', ''),
                dados.get('capital_social', ''),
                dados.get('porte', {}).get('descricao', ''),
                dados.get('natureza_juridica', {}).get('descricao', ''),
                determinar_natureza_tipo(dados),  # Adiciona o tipo de natureza
                determinar_tipo(dados),  # Adiciona o tipo (Filial ou Matriz)
                est.get('atividade_principal', {}).get('descricao', ''),
                cidade.get('nome', ''),
                estado.get('sigla', '')
            ])
    except Exception as e:
        print(f"Erro ao salvar dados no CSV: {e}")

def menu():
    arquivo_csv = 'cnpj5.csv'
    while True:
        print("\nMenu")
        print("1. Inserir CNPJ")
        print("2. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cnpj = input("Digite o CNPJ (somente números): ")
            dados = obter_dados_cnpj(cnpj)
            if dados:
                salvar_em_csv(cnpj, dados, arquivo_csv)  # Passa o CNPJ junto com os dados
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