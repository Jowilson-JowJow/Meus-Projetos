# 🚲 Sistema de Gerenciamento — Oficina de Bicicletas

Sistema desktop desenvolvido em Python com interface gráfica PySide6 e banco de dados MySQL,
utilizando a arquitetura MVC (Model-View-Controller).

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **PySide6** — interface gráfica (Qt Designer)
- **MySQL** — banco de dados
- **mysql-connector-python** — conexão Python ↔ MySQL

---

## 📁 Estrutura do Projeto

```
oficina_bike/
│
├── main.py                        # Ponto de entrada do sistema
├── requirements.txt               # Dependências do projeto
├── LEIA-ME.md                     # Este arquivo
│
├── database/
│   ├── conexao.py                 # Configuração da conexão com o MySQL
│   └── banco.sql                  # Script de criação do banco e tabelas
│
├── models/
│   ├── usuario_model.py           # CRUD de usuários
│   ├── cliente_model.py           # CRUD de clientes
│   ├── bicicleta_model.py         # CRUD de bicicletas
│   └── servico_model.py           # CRUD de serviços
│
├── controllers/
│   ├── login_controller.py        # Controle da tela de login
│   ├── home_controller.py         # Controle do menu e usuários
│   ├── cliente_controller.py      # Controle da tela de clientes
│   ├── bicicleta_controller.py    # Controle da tela de bicicletas
│   ├── servico_controller.py      # Controle da tela de serviços
│   └── relatorio_controller.py    # Controle da tela de relatórios
│
├── views/
│   ├── login.ui                   # Tela de login (Qt Designer)
│   └── home.ui                    # Tela principal com todas as páginas
│
└── services/
    └── validacoes.py              # Funções de validação reutilizáveis
```

---

## ⚙️ Como Instalar e Executar

### 1. Pré-requisitos

- Python 3.10 ou superior instalado
- MySQL instalado e rodando
- MySQL Workbench (recomendado para executar o banco)

### 2. Criar o banco de dados

Abra o **MySQL Workbench**, vá em:

```
File → Open SQL Script → selecione o arquivo database/banco.sql → clique em Execute (⚡)
```

Isso criará o banco `sistema` com todas as tabelas e o usuário padrão.

### 3. Instalar as dependências Python

No terminal, dentro da pasta do projeto:

```bash
pip install -r requirements.txt
```

### 4. Executar o sistema

```bash
python main.py
```

---

## 🔐 Acesso Padrão

| Campo  | Valor               |
|--------|---------------------|
| E-mail | admin@oficina.com   |
| Senha  | 1234                |

> ⚠️ Recomenda-se criar um novo usuário após o primeiro acesso.

---

## 📋 Funcionalidades

- [x] Login com autenticação no banco de dados
- [x] Cadastro, edição e listagem de **Usuários**
- [x] Cadastro, edição e listagem de **Clientes**
- [x] Cadastro, edição e listagem de **Bicicletas** (vinculadas a clientes)
- [x] Cadastro, edição e listagem de **Serviços** (vinculados a bicicletas)
- [x] Tela de **Relatórios** com totais por status e valor

---

## 🗄️ Banco de Dados

O sistema utiliza **MySQL** com o banco chamado `sistema`.

Tabelas criadas pelo `banco.sql`:

| Tabela      | Descrição                                      |
|-------------|------------------------------------------------|
| `usuarios`  | Usuários que acessam o sistema (login)         |
| `clientes`  | Clientes da oficina                            |
| `bicicletas`| Bicicletas dos clientes                        |
| `servicos`  | Serviços realizados nas bicicletas             |

---

## 👨‍💻 Arquitetura

O projeto segue o padrão **MVC**:

| Camada         | Responsabilidade                                      |
|----------------|-------------------------------------------------------|
| **Model**      | Acessa o banco de dados (SELECT, INSERT, UPDATE, DELETE) |
| **View**       | Interface gráfica criada no Qt Designer (arquivos .ui)   |
| **Controller** | Captura eventos da tela, valida dados e chama os Models  |

---

*Projeto desenvolvido como atividade acadêmica — Python com arquitetura MVC.*