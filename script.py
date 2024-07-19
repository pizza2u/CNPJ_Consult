import time
import requests
import csv
from tqdm import tqdm

def data(cnpj):
    url = f"https://publica.cnpj.ws/cnpj/{cnpj}" # API pública
    try:
        response = requests.get(url)
        response.raise_for_status() #  se bem sucedida retorna 200
        dados = response.json() # retorna pela em JSON.
       # print(dados)  verificar o JSON
        return dados
    except requests.RequestException as e:
        print(f"Erro ao obter dados: {e}") #caso de falha ou limites atingidos
        return None

def type(natureza_juridica): #tipo de natureza (Municipal, Estadual, Federal)
    if natureza_juridica:
        descricao = natureza_juridica.lower()
        if 'municipal' or 'Município' in descricao:
            return 'Municipal'
        elif 'estadual' in descricao:
            return 'Estadual'
        elif 'federal' in descricao:
            return 'Federal'
    return 'Não Especificado'  #se não for nenhum dos tipos

def save(cnpj, dados, arquivo):
    try:
        with open(arquivo, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # arquivo vazio para cabeçalho
                writer.writerow([
                    'CNPJ', 'Razão Social', 'Porte', 
                    'Natureza Jurídica', 'Natureza Tipo', 'Tipo(Matriz/Filial)', 
                    'Atividade Principal', 'Município', 'UF'
                ])
            
            est = dados.get('estabelecimento', {})
            cidade = est.get('cidade', {})
            estado = est.get('estado', {})
            
            writer.writerow([
                cnpj,  # CNPJ digitado pelo usuário
                dados.get('razao_social', ''),
                dados.get('porte', {}).get('descricao', ''), 
                dados.get('natureza_juridica', {}).get('descricao', ''), # natureza juridica
                type(dados.get('natureza_juridica', {}).get('descricao', '')),  #  tipo de natureza
                est.get('tipo', ''),  # tipo (Filial ou Matriz)
                est.get('atividade_principal', {}).get('descricao', ''),
                cidade.get('nome', '') if cidade else '',  # Verifica se cidade não é None e adc o nome
                estado.get('sigla', '') if estado else '',  # Verifica se estado não é None e adc a UF
            ])
    except AttributeError as e:
        print(f"Erro ao acessar(dados nulos): {e}") # EM CASO DE DADOS NULOS
    except Exception as e:
        print(f"Erro ao salvar dados: {e}") # no CSV

def menu():
    arquivo_csv = 'dados.csv' # escolhe o nome do arquivo que vai ser salvo os dados
    while True:
        print("\nMenu")
        print("1. Inserir CNPJ")
        print("2. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cnpj = input("Digite o CNPJ (somente números): ")
            dados = data(cnpj)
            if dados:
                save(cnpj, dados, arquivo_csv) 
                print("Dados salvos com sucesso!")
            else:
                print("Não foi possível obter os dados do CNPJ.")
        elif opcao == '2':
            for i in tqdm(range(10), desc="Carregando"):
                time.sleep(0.05)
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

menu()
