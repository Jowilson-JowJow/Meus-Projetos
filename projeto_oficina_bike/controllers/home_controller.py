import os
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QMessageBox
from models.usuario_model import UsuarioModel
from services.validacoes import campo_vazio, senhas_iguais

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIEW_DIR = os.path.join(BASE_DIR, "..", "views")

class HomeController:

    def __init__(self):
        loader = QUiLoader()
        file = QFile(os.path.join(VIEW_DIR, "home.ui"))
        file.open(QFile.ReadOnly)
        self.window = loader.load(file)
        file.close()

        self.model = UsuarioModel()
        self.usuario_id_selecionado = None

        # Índice inicial: Home (0)
        self.window.stackedWidget.setCurrentIndex(0)

        # --- Menu lateral ---
        self.window.btnMenuHome.clicked.connect(self.ir_home)
        self.window.btnMenuUsuarios.clicked.connect(self.listar_usuarios)
        self.window.btnMenuClientes.clicked.connect(self.abrir_clientes)
        self.window.btnMenuBicicletas.clicked.connect(self.abrir_bicicletas)
        self.window.btnMenuServicos.clicked.connect(self.abrir_servicos)
        self.window.btnMenuRelatorios.clicked.connect(self.abrir_relatorios)

        # --- Usuários ---
        self.window.btnUsuariosNovo.clicked.connect(self.novo_usuario)
        self.window.btnCadUsuarioCadastrar.clicked.connect(self.salvar_usuario)
        self.window.btnCadUsuarioVoltar.clicked.connect(self.listar_usuarios)
        self.window.tabelaUsuarios.cellDoubleClicked.connect(self.abrir_edicao_usuario)

    # ── Navegação ──────────────────────────────────────────────
    def ir_home(self):
        self.window.stackedWidget.setCurrentIndex(0)

    def abrir_clientes(self):
        from controllers.cliente_controller import ClienteController
        self.cliente_ctrl = ClienteController(self.window)
        self.cliente_ctrl.listar()

    def abrir_bicicletas(self):
        from controllers.bicicleta_controller import BicicletaController
        self.bicicleta_ctrl = BicicletaController(self.window)
        self.bicicleta_ctrl.listar()

    def abrir_servicos(self):
        from controllers.servico_controller import ServicoController
        self.servico_ctrl = ServicoController(self.window)
        self.servico_ctrl.listar()

    def abrir_relatorios(self):
        from controllers.relatorio_controller import RelatorioController
        self.relatorio_ctrl = RelatorioController(self.window)
        self.relatorio_ctrl.carregar()

    # ── Usuários ───────────────────────────────────────────────
    def listar_usuarios(self):
        self.usuario_id_selecionado = None
        self.window.stackedWidget.setCurrentIndex(1)
        dados = self.model.listar()

        self.window.tabelaUsuarios.setRowCount(len(dados))
        self.window.tabelaUsuarios.verticalHeader().setVisible(False)
        self.window.tabelaUsuarios.setSelectionBehavior(
            self.window.tabelaUsuarios.SelectionBehavior.SelectRows
        )
        self.window.tabelaUsuarios.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for linha, usuario in enumerate(dados):
            self.window.tabelaUsuarios.setItem(linha, 0, QTableWidgetItem(str(usuario[0])))
            self.window.tabelaUsuarios.setItem(linha, 1, QTableWidgetItem(usuario[1]))
            self.window.tabelaUsuarios.setItem(linha, 2, QTableWidgetItem(usuario[2]))
            self.window.tabelaUsuarios.setItem(linha, 3, QTableWidgetItem(usuario[3]))

    def novo_usuario(self):
        self.usuario_id_selecionado = None
        self.window.inputCadUsuarioNome.clear()
        self.window.inputCadUsuarioEmail.clear()
        self.window.inputCadUsuarioSenha.clear()
        self.window.inputCadUsuarioConfirmarSenha.clear()
        self.window.stackedWidget.setCurrentIndex(2)

    def abrir_edicao_usuario(self, row):
        self.usuario_id_selecionado = int(self.window.tabelaUsuarios.item(row, 0).text())
        nome  = self.window.tabelaUsuarios.item(row, 1).text()
        email = self.window.tabelaUsuarios.item(row, 2).text()
        senha = self.window.tabelaUsuarios.item(row, 3).text()

        self.window.inputCadUsuarioNome.setText(nome)
        self.window.inputCadUsuarioEmail.setText(email)
        self.window.inputCadUsuarioSenha.setText(senha)
        self.window.inputCadUsuarioConfirmarSenha.setText(senha)
        self.window.stackedWidget.setCurrentIndex(2)

    def salvar_usuario(self):
        nome             = self.window.inputCadUsuarioNome.text()
        email            = self.window.inputCadUsuarioEmail.text()
        senha            = self.window.inputCadUsuarioSenha.text()
        confirmar_senha  = self.window.inputCadUsuarioConfirmarSenha.text()

        if campo_vazio(nome, email, senha, confirmar_senha):
            QMessageBox.warning(self.window, "Atenção", "Preencha todos os campos!")
            return

        if not senhas_iguais(senha, confirmar_senha):
            QMessageBox.warning(self.window, "Atenção", "As senhas não são iguais!")
            return

        if self.usuario_id_selecionado:
            self.model.atualizar(self.usuario_id_selecionado, nome, email, senha)
            QMessageBox.information(self.window, "Sucesso", "Usuário atualizado com sucesso!")
        else:
            self.model.inserir(nome, email, senha)
            QMessageBox.information(self.window, "Sucesso", "Usuário cadastrado com sucesso!")

        self.listar_usuarios()

    def show(self):
        self.window.show()
