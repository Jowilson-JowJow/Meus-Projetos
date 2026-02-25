import tkinter as tk

def limpar():
    inputDisplay.delete(0, tk.END)

def calcular():    
    try:
        resultado= eval(inputDisplay.get())
        limpar()
        inputDisplay.insert(0,str(resultado))
    except:
        limpar()
        inputDisplay.insert(0,"ERROR")

def adicionar(valor):
    inputDisplay.insert(tk.END, valor)


janela = tk.Tk()
janela.title("Calculadora")
janela.geometry("200x280")

inputDisplay = tk.Entry(janela, font=("Arial", 20), width=12, bd=5, justify="right")
inputDisplay.grid(row=0, column=0, columnspan=4, padx=3,pady=2)

botoes = [
    ("7",1,0),("8",1,1),("9",1,2),("/",1,3),
    ("4",2,0),("5",2,1),("6",2,2),("*",2,3),
    ("1",3,0),("2",3,1),("3",3,2),("-",3,3),
    (".",4,0),("0",4,1),("=",4,2),("+",4,3),
]

for(texto, linha, coluna) in botoes:
    if texto == "=":
        tk.Button(janela, text=texto, width=5, height=2, command=calcular).grid(row=linha, column=coluna, padx=2,pady=1)
    else:
        tk.Button(janela, text=texto, width=5, height=2, command=lambda t=texto: adicionar(t)).grid(row=linha, column=coluna, padx=2, pady=1)

botaoLimpar= tk.Button(janela, text="C", width=26, height=2, bg="red", fg="white",command=limpar).grid(row=5, column=0, columnspan=4, padx=2, pady=1)

janela.mainloop() #para manter a tela sempre aberta