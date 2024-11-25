import tkinter as tk
from tkinter import messagebox
import math

def clicar_botao(valor):
    texto_atual = entrada_exibicao.get()
    entrada_exibicao.delete(0, tk.END)
    entrada_exibicao.insert(0, texto_atual + str(valor))

def calcular_resultado():
    try:
        expressao = entrada_exibicao.get()
        resultado = eval(expressao)
        entrada_exibicao.delete(0, tk.END)
        entrada_exibicao.insert(0, str(resultado))
    except Exception:
        messagebox.showerror("Erro", "Expressão inválida!")
        entrada_exibicao.delete(0, tk.END)

def limpar_entrada():
    entrada_exibicao.delete(0, tk.END)

def operacao_cientifica(operacao):
    try:
        valor = float(entrada_exibicao.get())
        if operacao == "raiz":
            resultado = math.sqrt(valor)
        elif operacao == "log":
            if valor > 0:
                resultado = math.log(valor)
            else:
                raise ValueError("Número deve ser maior que zero!")
        elif operacao == "seno":
            resultado = math.sin(math.radians(valor))
        elif operacao == "cosseno":
            resultado = math.cos(math.radians(valor))
        elif operacao == "tangente":
            resultado = math.tan(math.radians(valor))
        entrada_exibicao.delete(0, tk.END)
        entrada_exibicao.insert(0, str(resultado))
    except ValueError as ve:
        messagebox.showerror("Erro", str(ve))
    except Exception:
        messagebox.showerror("Erro", "Entrada inválida!")

janela = tk.Tk()
janela.title("Calculadora Científica")

entrada_exibicao = tk.Entry(janela, font=("Arial", 20), borderwidth=5, relief=tk.RIDGE, justify="right")
entrada_exibicao.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

botoes = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3)
]

for (texto, linha, coluna) in botoes:
    if texto == '=':
        tk.Button(janela, text=texto, width=5, height=2, font=("Arial", 15), command=calcular_resultado)\
            .grid(row=linha, column=coluna, padx=5, pady=5)
    else:
        tk.Button(janela, text=texto, width=5, height=2, font=("Arial", 15),
                  command=lambda t=texto: clicar_botao(t)).grid(row=linha, column=coluna, padx=5, pady=5)

botoes_cientificos = [
    ('√', 'raiz', 5, 0), ('log', 'log', 5, 1),
    ('sen', 'seno', 5, 2), ('cos', 'cosseno', 5, 3), ('tan', 'tangente', 6, 0)
]

for (texto, operacao, linha, coluna) in botoes_cientificos:
    tk.Button(janela, text=texto, width=5, height=2, font=("Arial", 15),
              command=lambda o=operacao: operacao_cientifica(o)).grid(row=linha, column=coluna, padx=5, pady=5)

tk.Button(janela, text="C", width=5, height=2, font=("Arial", 15), command=limpar_entrada)\
    .grid(row=6, column=1, padx=5, pady=5)

janela.mainloop()
