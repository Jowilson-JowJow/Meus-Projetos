from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QMessageBox
from models.servico_model import ServicoModel
from models.bicicleta_model import BicicletaModel
from services.validacoes import campo_vazio, valor_valido

class ServicoController:

    def __init__(self, window):
        self.window = window
        self.model = ServicoModel()
        self.bicicleta_model = BicicletaModel()
        self.servico_id_selecionado = None

        self.window.btnServicosNovo.clicked.connect(self.novo_servico)
        self.window.btnCadServicoCadastrar.clicked.connect(self.salvar_servico)
        self.window.btnCadServicoVoltar.clicked.connect(self.listar)
        self.window.tabelaServicos.cellDoubleClicked.connect(self.abrir_edicao)

    def listar(self):
        self.servico_id_selecionado = None
        self.window.stackedWidget.setCurrentIndex(7)
        dados = self.model.listar()

        self.window.tabelaServicos.setRowCount(len(dados))
        self.window.tabelaServicos.verticalHeader().setVisible(False)
        self.window.tabelaServicos.setSelectionBehavior(
            self.window.tabelaServicos.SelectionBehavior.SelectRows
        )
        self.window.tabelaServicos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for linha, servico in enumerate(dados):
            self.window.tabelaServicos.setItem(linha, 0, QTableWidgetItem(str(servico[0])))
            self.window.tabelaServicos.setItem(linha, 1, QTableWidgetItem(servico[1]))
            self.window.tabelaServicos.setItem(linha, 2, QTableWidgetItem(f"{servico[2]} {servico[3]}"))
            self.window.tabelaServicos.setItem(linha, 3, QTableWidgetItem(servico[4]))
            self.window.tabelaServicos.setItem(linha, 4, QTableWidgetItem(f"R$ {servico[5]:.2f}"))
            self.window.tabelaServicos.setItem(linha, 5, QTableWidgetItem(servico[6]))

    def carregar_combo_bicicletas(self):
        self.window.comboCadServicoBicicleta.clear()
        bicicletas = self.bicicleta_model.listar()
        for b in bicicletas:
            self.window.comboCadServicoBicicleta.addItem(f"{b[2]} {b[3]} - {b[1]}", b[0])

    def novo_servico(self):
        self.servico_id_selecionado = None
        self.carregar_combo_bicicletas()
        self.window.inputCadServicoDescricao.clear()
        self.window.inputCadServicoValor.clear()
        self.window.comboCadServicoStatus.setCurrentIndex(0)
        self.window.inputCadServicoDataEntrada.clear()
        self.window.inputCadServicoDataSaida.clear()
        self.window.stackedWidget.setCurrentIndex(8)

    def abrir_edicao(self, row):
        self.servico_id_selecionado = int(self.window.tabelaServicos.item(row, 0).text())
        self.carregar_combo_bicicletas()
        self.window.inputCadServicoDescricao.setText(self.window.tabelaServicos.item(row, 3).text())
        valor_texto = self.window.tabelaServicos.item(row, 4).text().replace("R$ ", "")
        self.window.inputCadServicoValor.setText(valor_texto)
        status = self.window.tabelaServicos.item(row, 5).text()
        idx = self.window.comboCadServicoStatus.findText(status)
        if idx >= 0:
            self.window.comboCadServicoStatus.setCurrentIndex(idx)
        self.window.stackedWidget.setCurrentIndex(8)

    def salvar_servico(self):
        bicicleta_id  = self.window.comboCadServicoBicicleta.currentData()
        descricao     = self.window.inputCadServicoDescricao.text()
        valor         = self.window.inputCadServicoValor.text()
        status        = self.window.comboCadServicoStatus.currentText()
        data_entrada  = self.window.inputCadServicoDataEntrada.text()
        data_saida    = self.window.inputCadServicoDataSaida.text()

        if not bicicleta_id or campo_vazio(descricao, valor, data_entrada):
            QMessageBox.warning(self.window, "Atenção", "Bicicleta, descrição, valor e data de entrada são obrigatórios!")
            return

        if not valor_valido(valor):
            QMessageBox.warning(self.window, "Atenção", "Informe um valor numérico válido!")
            return

        valor_float = float(valor.replace(",", "."))
        data_saida = data_saida if data_saida.strip() else None

        if self.servico_id_selecionado:
            self.model.atualizar(self.servico_id_selecionado, bicicleta_id, descricao, valor_float, status, data_entrada, data_saida)
            QMessageBox.information(self.window, "Sucesso", "Serviço atualizado com sucesso!")
        else:
            self.model.inserir(bicicleta_id, descricao, valor_float, status, data_entrada, data_saida)
            QMessageBox.information(self.window, "Sucesso", "Serviço cadastrado com sucesso!")

        self.listar()
