import requests
import csv
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

def obter_dados_cnpj(cnpj):
    url = f"https://publica.cnpj.ws/cnpj/{cnpj}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        dados = response.json()
        return dados
    except requests.RequestException as e:
        print(f"Erro ao obter dados: {e}")
        return None

def determinar_natureza_tipo(natureza_juridica):
    """Função para determinar o tipo de natureza (Municipal, Estadual, Federal)."""
    if natureza_juridica:
        descricao = natureza_juridica.lower()
        if 'municipal' in descricao:
            return 'Municipal'
        elif 'estadual' in descricao:
            return 'Estadual'
        elif 'federal' in descricao:
            return 'Federal'
    return 'Não Especificado'

def salvar_em_csv(cnpj, dados, arquivo):
    try:
        # Escrever no arquivo CSV (substitui o conteúdo existente)
        with open(arquivo, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'CNPJ', 'Razão Social', 'Porte', 
                'Natureza Jurídica', 'Natureza Tipo', 'Tipo(Matriz/Filial)', 
                'Atividade Principal', 'Município', 'UF'
            ])
            
            est = dados.get('estabelecimento', {})
            cidade = est.get('cidade', {})
            estado = est.get('estado', {})
            inscricoes_estaduais = dados.get('inscricoes_estaduais', [{}])[0]
            simples = dados.get('simples', {})
            
            writer.writerow([
                cnpj,  # Adiciona o CNPJ digitado pelo usuário
                dados.get('razao_social', ''),
                dados.get('porte', {}).get('descricao', ''),
                dados.get('natureza_juridica', {}).get('descricao', ''),
                determinar_natureza_tipo(dados.get('natureza_juridica', {}).get('descricao', '')),  # Adiciona o tipo de natureza
                est.get('tipo', ''),  # Tipo (Filial ou Matriz)
                est.get('atividade_principal', {}).get('descricao', ''),
                cidade.get('nome', '') if cidade else '',  # Verifica se cidade não é None
                estado.get('sigla', '') if estado else '',  # Verifica se estado não é None
            ])
        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
    except AttributeError as e:
        print(f"Erro ao acessar um atributo em dados nulos: {e}")
    except Exception as e:
        print(f"Erro ao salvar dados no CSV: {e}")

def buscar_dados():
    cnpj = entry_cnpj.get()
    dados = obter_dados_cnpj(cnpj)
    if dados:
        salvar_em_csv(cnpj, dados, arquivo_csv)
    else:
        messagebox.showerror("Erro", "Não foi possível obter os dados do CNPJ.")

def selecionar_arquivo():
    global arquivo_csv
    arquivo_csv = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")],
                                             title="Escolha o arquivo CSV")
    label_arquivo.config(text=f"Arquivo: {arquivo_csv}")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Consulta CNPJ")

# Variáveis
arquivo_csv = "DADOS2.csv"

# Layout
tk.Label(root, text="Digite o CNPJ (somente números):").pack(pady=10)
entry_cnpj = tk.Entry(root)
entry_cnpj.pack(pady=5)

tk.Button(root, text="Buscar Dados", command=buscar_dados).pack(pady=10)

tk.Button(root, text="Selecionar Arquivo CSV", command=selecionar_arquivo).pack(pady=5)
label_arquivo = tk.Label(root, text=f"Arquivo: {arquivo_csv}")
label_arquivo.pack(pady=5)

tk.Button(root, text="Sair", command=root.quit).pack(pady=10)

root.mainloop()
