import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector # Biblioteca para conectar ao banco de dados MySQL

# Função para estabelecer a conexão com o banco de dados MySQL
def conectar(): 
    return mysql.connector.connect(
        host = "localhost",
        user="root",
        password = "",
        database = "db_usuario"
    )

# Função para buscar os dados no banco e atualizar a visualização na tabela (Treeview)
def carregar_dados():
    # Limpa todos os itens atuais da tabela antes de recarregar
    for item in tabela.get_children():
        tabela.delete(item)

    conn = conectar()
    cursor = conn.cursor()
    # Seleciona todos os registros da tabela db_usuarios
    cursor.execute("SELECT * FROM db_usuarios")
    # Insere cada linha retornada do banco dentro da tabela da interface
    for linha in cursor.fetchall():
        tabela.insert("","end", values=linha)
    conn.close()

# Função para cadastrar um novo usuário no banco de dados
def novo_usuario():
    # Obtém os valores digitados nos campos de entrada
    nome = input_nome.get()
    email = input_email.get()
    endereco = input_endereco.get()

    # Validação simples para garantir que campos obrigatórios não fiquem vazios
    if nome == "" or email == "" or endereco =="":
        messagebox.showwarning("Aviso", "Nome, Email e Endereço são obrigatorios")
        return
    
    conn = conectar()
    cursor = conn.cursor()
    # Executa o comando SQL de inserção usando placeholders (%s) por segurança
    cursor.execute("INSERT INTO db_usuarios (nome, email, endereco) VALUES (%s, %s, %s)", (nome, email, endereco))
    conn.commit() # Confirma a alteração no banco
    conn.close()

    carregar_dados() # Atualiza a tabela visual
    limpar_campos()  # Limpa os campos do formulário

# Função para atualizar os dados de um usuário já existente
def editar_usuario():
    selecionado = tabela.selection() # Verifica se há algum item selecionado na tabela

    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um Usuario")
        return
    
    # Coleta os novos dados dos campos de entrada
    id_usuario = input_id.get()
    nome = input_nome.get()
    email = input_email.get()
    endereco = input_endereco.get()

    conn = conectar()
    cursor = conn.cursor()
    # Atualiza o registro baseado no ID que está no campo readonly
    cursor.execute("UPDATE db_usuarios SET nome=%s, email=%s, endereco=%s WHERE id=%s", (nome, email, endereco, id_usuario))
    conn.commit()
    conn.close()

    carregar_dados() # Atualiza a lista
    limpar_campos()

# Função para remover um usuário do banco de dados
def excluir_usuario():
    selecionado = tabela.selection()

    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um Usuario")
        return
    
    # Exibe uma caixa de diálogo para confirmar a exclusão
    confirmar = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este usuário?")

    if confirmar:
        item = tabela.item(selecionado)
        id_usuario = item['values'][0] # Obtém o ID da linha selecionada

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM db_usuarios WHERE id=%s", (id_usuario,))
        conn.commit()
        conn.close()

        tabela.delete(selecionado) # Remove da visualização imediata
        limpar_campos()
        messagebox.showinfo("SUcesso", "Usuário removido com sucesso!")

# Função chamada quando o usuário clica em uma linha da tabela
def selecionar_usuario(event):
    selecionado = tabela.selection()
    limpar_campos()
    if selecionado:
        valores = tabela.item(selecionado, "values")
        # O ID é readonly, então precisamos habilitar (normal) para inserir e bloquear (readonly) depois
        input_id.config(state="normal")
        input_id.insert(0, valores[0])
        input_id.config(state="readonly")
        
        # Preenche os demais campos com os dados da linha selecionada
        input_nome.insert(0, valores[1])
        input_email.insert(0, valores[2])
        input_endereco.insert(0, valores[3])

# Função para resetar todos os campos de entrada do formulário
def limpar_campos():
    input_id.config(state="normal") # Habilita para permitir a limpeza
    input_id.delete(0, tk.END)
    input_id.config(state="readonly")
    input_nome.delete(0, tk.END)
    input_email.delete(0, tk.END)
    input_endereco.delete(0, tk.END)

# Configurações principais da janela Tkinter
janela = tk.Tk()
janela.title("Cadastro de Usuario")
janela.geometry("750x450")

# Criação do container (Frame) para organizar os rótulos e campos de entrada
frame_form = tk.Frame(janela)
frame_form.pack(pady=10)

# Definição dos rótulos (Labels) e campos de entrada (Entries) usando o sistema de grade (Grid)
tk.Label(frame_form, text="ID").grid(row=0, column=0, padx=5, sticky="e")
input_id = tk.Entry(frame_form, width=20, state="readonly")
input_id.grid(row=0, column=1, padx=20)

tk.Label(frame_form, text="Nome").grid(row=1, column=0, padx=5, sticky="e")
input_nome = tk.Entry(frame_form, width=20)
input_nome.grid(row=1, column=1, padx=20)

tk.Label(frame_form, text="Email").grid(row=2, column=0, padx=5, sticky="e")
input_email = tk.Entry(frame_form, width=20)
input_email.grid(row=2, column=1, padx=20)

tk.Label(frame_form, text="Endereço").grid(row=3, column=0, padx=5, sticky="e")
input_endereco = tk.Entry(frame_form, width=20)
input_endereco.grid(row=3, column=1, padx=20)

# Container para organizar os botões de ação
frame_button = tk.Frame(janela)
frame_button.pack(pady=10)

# Botões que chamam as funções definidas anteriormente
btn_novo = tk.Button(frame_button, text="Cadastro", width=10, command=novo_usuario).grid(row=0, column=0, padx=5)
btn_editar = tk.Button(frame_button, text="Editar", width=10, command=editar_usuario).grid(row=0, column=1, padx=5)
btn_excluir = tk.Button(frame_button, text="Excluir", width=10, command=excluir_usuario).grid(row=0, column=2, padx=5)
btn_limpar = tk.Button(frame_button, text="Limpar", width=10, command=limpar_campos).grid(row=0, column=3, padx=5)

# Configuração da Tabela (Treeview) para exibição dos dados
colunas = ("ID", "NOME","EMAIL", "ENDEREÇO")
tabela = ttk.Treeview(janela, columns=colunas, show="headings")

# Define os cabeçalhos e a largura das colunas
for col in colunas:
    tabela.heading(col, text=col)
    tabela.column(col, width=170)

tabela.pack(fill="both", expand=True, padx=20, pady=20)

# Vincula o evento de clique na tabela à função selecionar_usuario
tabela.bind("<<TreeviewSelect>>", selecionar_usuario)

# Carrega os dados do banco assim que o programa inicia
carregar_dados()

# Inicia o loop principal da interface gráfica
janela.mainloop()


# para criar a tabela no mysql 
# create database db_usuario;
# use db_usuario;

# create table db_usuarios(
# id int not null primary key auto_increment,
# nome varchar(60) not null,
# email varchar (60) not null,
# endereco varchar (100) not null
# );
# select * from db_usuarios;