import tkinter as tk
import random
from tkinter import messagebox

tabuleiro = [""] * 9
jogo_ativo = False

vitorias_jogador = 0
vitorias_computador = 0
empates = 0

def iniciar_jogo():
    global jogo_ativo, tabuleiro

    tabuleiro = [""] * 9
    
    for i in range(1,10):
        globals()[f"btn{i}"].config(text="", state="normal")
    
    jogo_ativo = True
    jogada_computador()

def jogar(posicao):
    global jogo_ativo
    
    if not jogo_ativo:
        return
    
    if tabuleiro[posicao-1] == "":
        tabuleiro[posicao-1] = "O"
        globals()[f"btn{posicao}"].config(text="O", state="disabled")
        
        if verificar_vitoria("O"):
            finalizar_jogo("jogador")
            return
        
        if "" not in tabuleiro:
            finalizar_jogo("empate")
            return
        
        jogada_computador()

def jogada_computador():
    global jogo_ativo

    if not jogo_ativo:
        return
    
    posicoes_vazias = [i for i in range(9) if tabuleiro[i] == ""]
    
    if not posicoes_vazias:
        return
    
    pos = random.choice(posicoes_vazias)
    tabuleiro[pos] = "X"
    globals()[f"btn{pos+1}"].config(text="X", state="disabled")
    
    if verificar_vitoria("X"):
        finalizar_jogo("computador")
        return
        
    if "" not in tabuleiro:
        finalizar_jogo("empate")
        return

def verificar_vitoria(simbolo):
    combinacoes = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    
    for a,b,c in combinacoes:
        if tabuleiro[a] == tabuleiro[b] == tabuleiro[c] == simbolo:
            return True
    return False



def finalizar_jogo(resultado):
    global jogo_ativo, vitorias_jogador, vitorias_computador, empates
    
    jogo_ativo = False
    
    if resultado == "jogador":
        vitorias_jogador += 1
        messagebox.showinfo("status do Jogo", "Você Ganhou!!!")
    elif resultado == "computador":
        vitorias_computador += 1
        messagebox.showinfo("status do Jogo", "Você perdeu!!!")
    else:
        empates += 1
        messagebox.showinfo("status do Jogo", "Deu Velha!!!!")
    
    labelJogador.config(text=f"Vitórias Jogador: {vitorias_jogador}")
    labelCompt.config(text=f"Vitórias Computador: {vitorias_computador}")
    labelEmpate.config(text=f"Empates: {empates}")

    for i in range(1, 10):
        globals()[f"btn{i}"].config(state="disabled")




#criando a janela
janela= tk.Tk()
janela.title("Jogo da Velha by JowJow")
janela.geometry("400x500")

#criando o frame azul
frame = tk.Frame(janela, bg="blue", padx=20, pady=20)
frame.grid(sticky="nsew", row=0)

#criando o frame vermelho
frame1 = tk.Frame(janela, bg="red", padx=20, pady=20)
frame1.grid(sticky="nsew", row=1)

janela.grid_rowconfigure(0, weight=1)
janela.grid_columnconfigure(0, weight=1)

for i in range(3):
    frame.grid_rowconfigure(i, weight=1)
    frame.grid_columnconfigure(i, weight=1)

#criando botões utliziando uma lista de tulplas que serve para clicar e assim marcar o jogo da velha
botoes=[["",0,0,1],["",0,1,2],["",0,2,3],["",1,0,4],["",1,1,5],["",1,2,6],["",2,0,7],["",2,1,8],["",2,2,9]]


#criando botão do jogo da velha
for(texto, linha, coluna, pos) in botoes:
    globals()[f"btn{pos}"]=tk.Button(frame, text=texto, width=17, height=7, bg="white", command= lambda t=pos: jogar(t), font=("Arial",30))
    globals()[f"btn{pos}"].grid(row=linha,column=coluna, padx=5, pady=5, sticky=("nsew"))

#criando o botão de inicio do jogo
botoesInicio=["Start",0,0]

btnStart=tk.Button(frame1, text="Start", font=("Arial",20), width=5, height=1, bg="white", command=iniciar_jogo)
btnStart.grid(row=0,column=0, rowspan=3, padx=5, pady=5, sticky=("nsew"))

labelJogador = tk.Label(frame1, text="Vitórias Jogador: 0 ", bg="red", font=("Arial",15), fg="white")
labelJogador.grid(row=0,column=1, pady=2, padx=2, sticky="e")

labelCompt = tk.Label(frame1, text="Vitórias Computador: 0 ", bg="red", font=("Arial",15), fg="white")
labelCompt.grid(row=1,column=1, pady=2, padx=2, sticky="e")

labelEmpate = tk.Label(frame1, text="Empates: 0 ", bg="red", font=("Arial",15), fg="white")
labelEmpate.grid(row=2,column=1, pady=2, padx=2, sticky="e")

labelJogador.config(text=f"Vitórias Jogador: {vitorias_jogador}")


janela.mainloop()#matem a janela aberta, sempre a ultima linha do codigo.
