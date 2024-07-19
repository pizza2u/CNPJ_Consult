import tkinter as tk
from tkinter import messagebox
import requests
import csv

# Função para obter dados do CNPJ
def obter_dados_cnpj(cnpj):
    url = f"https://publica.cnpj.ws/cnpj/{cnpj}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        dados = response.json()
        return dados
    except requests.RequestException as e:
        messagebox.showerror("Erro", f"Erro ao obter dados: {e}")
        return None

# Função para salvar dados em CSV
def salvar_em_csv(cnpj, dados, arquivo):
    try:
        with open(arquivo, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Verifica se o arquivo está vazio para escrever o cabeçalho
                writer.writerow([
                    'CNPJ', 'Razão Social', 'Capital Social', 'Porte', 
                    'Natureza Jurídica', 'Atividade Principal', 'Município', 'UF'
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
                est.get('atividade_principal', {}).get('descricao', ''),
                cidade.get('nome', ''),
                estado.get('sigla', '')
            ])
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar dados no CSV: {e}")

# Função para lidar com o clique do botão
def obter_dados():
    cnpj = entry_cnpj.get().strip()
    if not cnpj.isdigit() or len(cnpj) != 14:
        messagebox.showwarning("Aviso", "Digite um CNPJ válido (14 dígitos).")
        return
    
    dados = obter_dados_cnpj(cnpj)
    if dados:
        salvar_em_csv(cnpj, dados, 'cnpj4.csv')
        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
    else:
        messagebox.showwarning("Aviso", "Não foi possível obter os dados do CNPJ.")

# Configuração da interface gráfica com tkinter
root = tk.Tk()
root.title("Consulta CNPJ")

# Layout da interface
tk.Label(root, text="Digite o CNPJ (somente números):").pack(pady=10)
entry_cnpj = tk.Entry(root, width=20)
entry_cnpj.pack(pady=5)

tk.Button(root, text="Obter Dados e Salvar", command=obter_dados).pack(pady=20)

# Inicia a aplicação
root.mainloop()
