import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
from PIL import Image, ImageTk  
janela = tk.Tk()
janela.title("Análise de Peças")
janela.geometry("1400x600")

def analisar_pecas(caminho_csv):
    try:
        dados = pd.read_csv(caminho_csv)

        resultados = []
        motivos = []

        for _, linha in dados.iterrows():
            id_peca = linha['ID']
            peso = linha['Peso (g)']
            tamanho = linha['Tamanho (cm)']
            acabamento = linha['Acabamento']

            if 50 <= peso <= 100 and 10 <= tamanho <= 20 and acabamento > 7:
                resultados.append("Aprovada")
                motivos.append("")
            else:
                resultados.append("Rejeitada")
                motivo = []
                if not (50 <= peso <= 100):
                    motivo.append("Peso fora dos limites")
                if not (10 <= tamanho <= 20):
                    motivo.append("Tamanho fora dos limites")
                if acabamento <= 7:
                    motivo.append("Acabamento insuficiente")
                motivos.append(", ".join(motivo))

        dados['Resultado'] = resultados
        dados['Motivo'] = motivos

        atualizar_tabela(dados)

        total_pecas = len(dados)
        total_rejeitadas = resultados.count("Rejeitada")
        percentual_rejeitadas = (total_rejeitadas / total_pecas) * 100
        percentual_aprovadas = 100 - percentual_rejeitadas

        if percentual_rejeitadas > 20:
            messagebox.showwarning("Alerta", "Mais de 20% das peças foram rejeitadas! Revisar processo.")

        dados.to_csv("resultado_analise.csv", index=False)
        info = tk.Label(janela, text=f"Total: {total_pecas} | " f"Aprovadas: {percentual_aprovadas:.2f}% | " f"Rejeitadas: {percentual_rejeitadas:.2f}%")
        info.pack(pady=20)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao analisar peças: {e}")

def atualizar_tabela(dados):
    for item in tabela.get_children():
        tabela.delete(item)

    for _, linha in dados.iterrows():
        tabela.insert("", tk.END, values=(
            linha['ID'], linha['Peso (g)'], linha['Tamanho (cm)'], linha['Acabamento'], linha['Resultado'], linha['Motivo']
        ))

def abrir_arquivo():
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
    if caminho:
        analisar_pecas(caminho)



# Adicionando o logotipo e o título.
frame_topo = tk.Frame(janela)
frame_topo.pack(pady=10)

try:
    imagem_logo = Image.open("img/logo.png")  # Caminho para a imagem do logotipo.
    imagem_logo = imagem_logo.resize((100, 100), Image.Resampling.LANCZOS)  # Redimensiona com LANCZOS.
    logo = ImageTk.PhotoImage(imagem_logo)
    label_logo = tk.Label(frame_topo, image=logo)
    label_logo.pack(side=tk.LEFT, padx=10)
except Exception as e:
    messagebox.showerror("Erro", f"Erro ao carregar a imagem do logotipo: {e}")

titulo = tk.Label(frame_topo, text="SENAI DEV EXPERIENCE - ETAPA FINAL 2024", font=("Arial", 18, "bold"))
titulo.pack(side=tk.LEFT)

botao_carregar = tk.Button(janela, text="Carregar base de dados", font=("Arial", 14), command=abrir_arquivo)
botao_carregar.pack(pady=10)

colunas = ('ID', 'Peso (g)', 'Tamanho (cm)', 'Acabamento', 'Resultado', 'Motivo')
tabela = ttk.Treeview(janela, columns=colunas, show='headings')

for coluna in colunas:
    tabela.heading(coluna, text=coluna)
    tabela.column(coluna, width=120)

tabela.pack(fill=tk.BOTH, expand=True, pady=10)

janela.mainloop()
