import csv
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

CSV_FILE = "despesas.csv"

def inicializar_csv():
    try:
        with open(CSV_FILE, "x", newline="") as file:
            escritor = csv.writer(file)
            escritor.writerow(["Data", "Categoria", "Valor", "Descrição"])
    except FileExistsError:
        pass

def adicionar_despesa(categoria, valor, descricao):
    data = datetime.datetime.now().strftime("%Y-%m-%d")
    with open(CSV_FILE, "a", newline="") as file:
        escritor = csv.writer(file)
        escritor.writerow([data, categoria, valor, descricao])
    messagebox.showinfo("Sucesso", "Despesa adicionada com sucesso!")
    atualizar_lista_despesas()

def limpar_despesas():
    with open(CSV_FILE, "w", newline="") as file:
        escritor = csv.writer(file)
        escritor.writerow(["Data", "Categoria", "Valor", "Descrição"])
    messagebox.showinfo("Sucesso", "Todas as despesas foram removidas!")
    atualizar_lista_despesas()

def visualizar_despesas():
    try:
        with open(CSV_FILE, "r") as file:
            leitor = csv.reader(file)
            return list(leitor)[1:]
    except FileNotFoundError:
        return []

def total_despesas():
    try:
        with open(CSV_FILE, "r") as file:
            leitor = csv.reader(file)
            next(leitor)
            total = sum(float(linha[2]) for linha in leitor)
            return f"Total de Despesas: R${total:.2f}"
    except (FileNotFoundError, IndexError, ValueError):
        return "Total de Despesas: R$0.00"

def atualizar_lista_despesas():
    for linha in arvore.get_children():
        arvore.delete(linha)
    for linha in visualizar_despesas():
        arvore.insert("", "end", values=linha)
    rotulo_total.config(text=total_despesas())

def enviar_despesa():
    categoria = entrada_categoria.get()
    valor = entrada_valor.get()
    descricao = entrada_descricao.get()
    if categoria and valor and descricao:
        try:
            adicionar_despesa(categoria, float(valor), descricao)
            entrada_categoria.delete(0, tk.END)
            entrada_valor.delete(0, tk.END)
            entrada_descricao.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "O valor deve ser um número válido.")
    else:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios.")

inicializar_csv()

# Configuração da Interface Gráfica
root = tk.Tk()
root.title("Controle de Gastos")
root.geometry("600x450")
root.configure(bg="#f5f5f5")

frame_superior = tk.Frame(root, bg="#4CAF50", pady=10)
frame_superior.pack(fill="x")

# Imagem ao lado do título
imagem_logo = ImageTk.PhotoImage(Image.open(r"C:/Users/LordSnorlax/Desktop/PRojeto/cofrinho.png").resize((30, 30)))  # Caminho da imagem logo
rotulo_imagem = tk.Label(frame_superior, image=imagem_logo, bg="#4CAF50")
rotulo_imagem.pack(side="left", padx=10)

rotulo_titulo = tk.Label(frame_superior, text="Controle de Gastos", font=("Arial", 16, "bold"), bg="#4CAF50", fg="white")
rotulo_titulo.pack(side="left", padx=10)

frame_principal = tk.Frame(root, padx=10, pady=10, bg="#f5f5f5")
frame_principal.pack(fill="both", expand=True)

tk.Label(frame_principal, text="Categoria:", bg="#f5f5f5").grid(row=0, column=0, sticky="w")
entrada_categoria = tk.Entry(frame_principal)
entrada_categoria.grid(row=0, column=1, pady=5)

tk.Label(frame_principal, text="Valor:", bg="#f5f5f5").grid(row=1, column=0, sticky="w")
entrada_valor = tk.Entry(frame_principal)
entrada_valor.grid(row=1, column=1, pady=5)

tk.Label(frame_principal, text="Descrição:", bg="#f5f5f5").grid(row=2, column=0, sticky="w")
entrada_descricao = tk.Entry(frame_principal)
entrada_descricao.grid(row=2, column=1, pady=5)

# Caminho das imagens
icone_adicionar = ImageTk.PhotoImage(Image.open(r"C:/Users/LordSnorlax/Desktop/PRojeto/capital.png").resize((20, 20)))
icone_limpar = ImageTk.PhotoImage(Image.open(r"C:/Users/LordSnorlax/Desktop/PRojeto/limpar-limpo.png").resize((20, 20)))

tk.Button(frame_principal, text=" Adicionar Despesa", command=enviar_despesa, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=10, image=icone_adicionar, compound="left").grid(row=3, column=0, columnspan=2, pady=10)

tk.Button(frame_principal, text=" Limpar Tudo", command=limpar_despesas, bg="#FF5733", fg="white", font=("Arial", 10, "bold"), padx=10, image=icone_limpar, compound="left").grid(row=4, column=0, columnspan=2, pady=10)

rotulo_total = tk.Label(frame_principal, text=total_despesas(), font=("Arial", 12, "bold"), bg="#f5f5f5", fg="#333")
rotulo_total.grid(row=5, column=0, columnspan=2, pady=10)

colunas = ("Data", "Categoria", "Valor", "Descrição")
arvore = ttk.Treeview(root, columns=colunas, show="headings")
for col in colunas:
    arvore.heading(col, text=col)
    arvore.column(col, width=120, anchor="center")

arvore.pack(expand=True, fill="both", padx=10, pady=10)

atualizar_lista_despesas()

root.mainloop()
