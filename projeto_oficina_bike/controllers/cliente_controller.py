from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QMessageBox
from models.cliente_model import ClienteModel
from services.validacoes import campo_vazio

class ClienteController:

    def __init__(self, window):
        self.window = window
        self.model = ClienteModel()
        self.cliente_id_selecionado = None

        self.window.btnClientesNovo.clicked.connect(self.novo_cliente)
        self.window.btnCadClienteCadastrar.clicked.connect(self.salvar_cliente)
        self.window.btnCadClienteVoltar.clicked.connect(self.listar)
        self.window.tabelaClientes.cellDoubleClicked.connect(self.abrir_edicao)

    def listar(self):
        self.cliente_id_selecionado = None
        self.window.stackedWidget.setCurrentIndex(3)
        dados = self.model.listar()

        self.window.tabelaClientes.setRowCount(len(dados))
        self.window.tabelaClientes.verticalHeader().setVisible(False)
        self.window.tabelaClientes.setSelectionBehavior(
            self.window.tabelaClientes.SelectionBehavior.SelectRows
        )
        self.window.tabelaClientes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for linha, cliente in enumerate(dados):
            self.window.tabelaClientes.setItem(linha, 0, QTableWidgetItem(str(cliente[0])))
            self.window.tabelaClientes.setItem(linha, 1, QTableWidgetItem(cliente[1]))
            self.window.tabelaClientes.setItem(linha, 2, QTableWidgetItem(cliente[2]))
            self.window.tabelaClientes.setItem(linha, 3, QTableWidgetItem(cliente[3]))
            self.window.tabelaClientes.setItem(linha, 4, QTableWidgetItem(cliente[4]))

    def novo_cliente(self):
        self.cliente_id_selecionado = None
        self.window.inputCadClienteNome.clear()
        self.window.inputCadClienteTelefone.clear()
        self.window.inputCadClienteEmail.clear()
        self.window.inputCadClienteEndereco.clear()
        self.window.stackedWidget.setCurrentIndex(4)

    def abrir_edicao(self, row):
        self.cliente_id_selecionado = int(self.window.tabelaClientes.item(row, 0).text())
        self.window.inputCadClienteNome.setText(self.window.tabelaClientes.item(row, 1).text())
        self.window.inputCadClienteTelefone.setText(self.window.tabelaClientes.item(row, 2).text())
        self.window.inputCadClienteEmail.setText(self.window.tabelaClientes.item(row, 3).text())
        self.window.inputCadClienteEndereco.setText(self.window.tabelaClientes.item(row, 4).text())
        self.window.stackedWidget.setCurrentIndex(4)

    def salvar_cliente(self):
        nome     = self.window.inputCadClienteNome.text()
        telefone = self.window.inputCadClienteTelefone.text()
        email    = self.window.inputCadClienteEmail.text()
        endereco = self.window.inputCadClienteEndereco.text()

        if campo_vazio(nome, telefone):
            QMessageBox.warning(self.window, "Atenção", "Nome e telefone são obrigatórios!")
            return

        if self.cliente_id_selecionado:
            self.model.atualizar(self.cliente_id_selecionado, nome, telefone, email, endereco)
            QMessageBox.information(self.window, "Sucesso", "Cliente atualizado com sucesso!")
        else:
            self.model.inserir(nome, telefone, email, endereco)
            QMessageBox.information(self.window, "Sucesso", "Cliente cadastrado com sucesso!")

        self.listar()
