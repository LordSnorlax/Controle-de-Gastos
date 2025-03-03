import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from deep_translator import GoogleTranslator
import docx

# Função para realizar a tradução
def traduzir(texto, idioma_destino):
    idiomas = {
        "Inglês": "en",
        "Espanhol": "es",
        "Francês": "fr",
        "Alemão": "de"
    }

    if idioma_destino not in idiomas:
        messagebox.showerror("Erro", "Idioma não suportado.")
        return ""

    try:
        traduzido = GoogleTranslator(source='auto', target=idiomas[idioma_destino]).translate(texto)
        return traduzido
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao traduzir: {e}")
        return ""

# Função para traduzir o texto da entrada
def traduzir_texto():
    texto = texto_entrada.get("1.0", tk.END).strip()
    idioma_destino = idioma_combobox.get()
    if not texto:
        messagebox.showwarning("Aviso", "Por favor, insira um texto para traduzir.")
        return
    traducao = traduzir(texto, idioma_destino)
    texto_saida.config(state=tk.NORMAL)
    texto_saida.delete("1.0", tk.END)
    texto_saida.insert(tk.END, traducao)
    texto_saida.config(state=tk.DISABLED)

# Função para carregar arquivo
def carregar_arquivo():
    arquivo = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt"), ("Arquivos Word", "*.docx")])
    if not arquivo:
        return

    texto = ""
    try:
        if arquivo.endswith(".txt"):
            with open(arquivo, "r", encoding="utf-8") as f:
                texto = f.read()
        elif arquivo.endswith(".docx"):
            doc = docx.Document(arquivo)
            for paragrafo in doc.paragraphs:
                texto += paragrafo.text + "\n"
        texto_entrada.delete("1.0", tk.END)
        texto_entrada.insert(tk.END, texto)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar arquivo: {e}")

# Configuração da Janela
janela = tk.Tk()
janela.title("Tradutor de Textos")
janela.geometry("600x500")
janela.resizable(False, False)

# Entrada de texto
ttk.Label(janela, text="Texto para Traduzir:").pack(pady=5)
texto_entrada = tk.Text(janela, height=5, width=70)
texto_entrada.pack(pady=5)

# Botão para carregar arquivo
ttk.Button(janela, text="Carregar Arquivo", command=carregar_arquivo).pack(pady=5)

# Seleção de Idioma
ttk.Label(janela, text="Idioma de Destino:").pack(pady=5)
idioma_combobox = ttk.Combobox(janela, values=["Inglês", "Espanhol", "Francês", "Alemão"])
idioma_combobox.pack(pady=5)
idioma_combobox.current(0)

# Botão Traduzir
ttk.Button(janela, text="Traduzir", command=traduzir_texto).pack(pady=10)

# Saída de texto traduzido
ttk.Label(janela, text="Texto Traduzido:").pack(pady=5)
texto_saida = tk.Text(janela, height=5, width=70, state=tk.DISABLED)
texto_saida.pack(pady=5)

# Inicializar a interface
janela.mainloop()
