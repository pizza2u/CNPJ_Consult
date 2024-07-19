import requests
import csv
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os

def data(cnpj):
    url = f"https://publica.cnpj.ws/cnpj/{cnpj}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        dados = response.json()
        return dados
    except requests.RequestException as e:
        print(f"Erro ao obter dados: {e}") #caso de falha ou limites atingidos
        return None

def type(natureza_juridica): #caso de falha ou limites atingidos
    if natureza_juridica:
        descricao = natureza_juridica.lower()
        if 'municipal' in descricao:
            return 'Municipal'
        elif 'estadual' in descricao:
            return 'Estadual'
        elif 'federal' in descricao:
            return 'Federal'
    return 'Não Especificado'

def save(cnpj, dados, arquivo):
    try:
        file_exists = os.path.isfile(arquivo)
        if file_exists:
            with open(arquivo, 'r', newline='', encoding='utf-8') as file:
                first_line = file.readline()
                if not first_line.strip():  # arquivo estiver vazio
                    file_exists = False
        
        with open(arquivo, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:  # poe cabeçalho se o arquivo estiver vazio
                writer.writerow([
                    'CNPJ', 'Razão Social', 'Porte', 
                    'Natureza Jurídica', 'Natureza Tipo', 'Tipo(Matriz/Filial)', 
                    'Atividade Principal', 'Município', 'UF'
                ])
            
            est = dados.get('estabelecimento', {})
            cidade = est.get('cidade', {})
            estado = est.get('estado', {})
            
            writer.writerow([
                cnpj,   # CNPJ digitado pelo usuário
                dados.get('razao_social', ''),
                dados.get('porte', {}).get('descricao', ''),
                dados.get('natureza_juridica', {}).get('descricao', ''),
                type(dados.get('natureza_juridica', {}).get('descricao', '')),  # natureza juridica
                est.get('tipo', ''),  # Tipo (Filial ou Matriz)
                est.get('atividade_principal', {}).get('descricao', ''),
                cidade.get('nome', '') if cidade else '',  # verifica se cidade não é None e adc o nome
                estado.get('sigla', '') if estado else '',  # verifica se estado não é None e adc a UF
            ])
    except AttributeError as e:
        print(f"Erro ao acessar(dados nulos): {e}") # EM CASO DE DADOS NULOS
    except Exception as e:
        print(f"Erro ao salvar dados: {e}") # no CSV

def source():
    cnpj = entry_cnpj.get()
    dados = data(cnpj)
    if dados:
        save(cnpj, dados, file_csv)
        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
    else:
        messagebox.showerror("Erro", "Não foi possível obter os dados do CNPJ.")

def file():
    global file_csv
    file_csv = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")],
                                             title="Escolha o arquivo CSV")
    label_arquivo.config(text=f"Arquivo: {file_csv}")

# INTERFACE TKINTER
root = tk.Tk()
root.title("Consulta CNPJ")

file_csv = "DADOS2.csv"

tk.Label(root, text="Digite o CNPJ (somente números):").pack(ipadx=80, ipady=20)
entry_cnpj = tk.Entry(root, borderwidth=2, relief="solid",width=20)
entry_cnpj.pack(pady=5)

tk.Button(root, text="Obter dados",bg='#00f234',borderwidth=2, relief="solid", command=source).pack(pady=10)

tk.Button(root, text="Selecionar Arquivo CSV existente", command=file).pack(pady=5)
label_arquivo = tk.Label(root, text=f"Arquivo (autocriação): {file_csv}") #exibir nome de arquivo selecionado
label_arquivo.pack(pady=5)

tk.Button(root, text="Sair", command=root.quit,bg='RED',borderwidth=2, relief="solid").pack(pady=10) #BOTÃO PARA SAIR

root.mainloop()
