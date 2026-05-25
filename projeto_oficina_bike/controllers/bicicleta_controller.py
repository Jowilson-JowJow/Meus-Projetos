from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QMessageBox
from models.bicicleta_model import BicicletaModel
from models.cliente_model import ClienteModel
from services.validacoes import campo_vazio

class BicicletaController:

    def __init__(self, window):
        self.window = window
        self.model = BicicletaModel()
        self.cliente_model = ClienteModel()
        self.bicicleta_id_selecionada = None

        self.window.btnBicicletasNovo.clicked.connect(self.nova_bicicleta)
        self.window.btnCadBicicletaCadastrar.clicked.connect(self.salvar_bicicleta)
        self.window.btnCadBicicletaVoltar.clicked.connect(self.listar)
        self.window.tabelaBicicletas.cellDoubleClicked.connect(self.abrir_edicao)

    def listar(self):
        self.bicicleta_id_selecionada = None
        self.window.stackedWidget.setCurrentIndex(5)
        dados = self.model.listar()

        self.window.tabelaBicicletas.setRowCount(len(dados))
        self.window.tabelaBicicletas.verticalHeader().setVisible(False)
        self.window.tabelaBicicletas.setSelectionBehavior(
            self.window.tabelaBicicletas.SelectionBehavior.SelectRows
        )
        self.window.tabelaBicicletas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for linha, bicicleta in enumerate(dados):
            self.window.tabelaBicicletas.setItem(linha, 0, QTableWidgetItem(str(bicicleta[0])))
            self.window.tabelaBicicletas.setItem(linha, 1, QTableWidgetItem(bicicleta[1]))
            self.window.tabelaBicicletas.setItem(linha, 2, QTableWidgetItem(bicicleta[2]))
            self.window.tabelaBicicletas.setItem(linha, 3, QTableWidgetItem(bicicleta[3]))
            self.window.tabelaBicicletas.setItem(linha, 4, QTableWidgetItem(bicicleta[4]))
            self.window.tabelaBicicletas.setItem(linha, 5, QTableWidgetItem(bicicleta[5]))

    def carregar_combo_clientes(self):
        self.window.comboCadBicicletaCliente.clear()
        clientes = self.cliente_model.listar()
        for cliente in clientes:
            self.window.comboCadBicicletaCliente.addItem(cliente[1], cliente[0])

    def nova_bicicleta(self):
        self.bicicleta_id_selecionada = None
        self.carregar_combo_clientes()
        self.window.inputCadBicicletaMarca.clear()
        self.window.inputCadBicicletaModelo.clear()
        self.window.inputCadBicicletaCor.clear()
        self.window.inputCadBicicletaNumeroSerie.clear()
        self.window.stackedWidget.setCurrentIndex(6)

    def abrir_edicao(self, row):
        self.bicicleta_id_selecionada = int(self.window.tabelaBicicletas.item(row, 0).text())
        self.carregar_combo_clientes()

        nome_cliente = self.window.tabelaBicicletas.item(row, 1).text()
        idx = self.window.comboCadBicicletaCliente.findText(nome_cliente)
        if idx >= 0:
            self.window.comboCadBicicletaCliente.setCurrentIndex(idx)

        self.window.inputCadBicicletaMarca.setText(self.window.tabelaBicicletas.item(row, 2).text())
        self.window.inputCadBicicletaModelo.setText(self.window.tabelaBicicletas.item(row, 3).text())
        self.window.inputCadBicicletaCor.setText(self.window.tabelaBicicletas.item(row, 4).text())
        self.window.inputCadBicicletaNumeroSerie.setText(self.window.tabelaBicicletas.item(row, 5).text())
        self.window.stackedWidget.setCurrentIndex(6)

    def salvar_bicicleta(self):
        cliente_id   = self.window.comboCadBicicletaCliente.currentData()
        marca        = self.window.inputCadBicicletaMarca.text()
        modelo       = self.window.inputCadBicicletaModelo.text()
        cor          = self.window.inputCadBicicletaCor.text()
        numero_serie = self.window.inputCadBicicletaNumeroSerie.text()

        if not cliente_id or campo_vazio(marca, modelo):
            QMessageBox.warning(self.window, "Atenção", "Cliente, marca e modelo são obrigatórios!")
            return

        if self.bicicleta_id_selecionada:
            self.model.atualizar(self.bicicleta_id_selecionada, cliente_id, marca, modelo, cor, numero_serie)
            QMessageBox.information(self.window, "Sucesso", "Bicicleta atualizada com sucesso!")
        else:
            self.model.inserir(cliente_id, marca, modelo, cor, numero_serie)
            QMessageBox.information(self.window, "Sucesso", "Bicicleta cadastrada com sucesso!")

        self.listar()
