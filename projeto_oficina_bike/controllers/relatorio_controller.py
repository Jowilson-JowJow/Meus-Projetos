from PySide6.QtWidgets import QTableWidgetItem, QHeaderView
from models.servico_model import ServicoModel

class RelatorioController:

    def __init__(self, window):
        self.window = window
        self.model = ServicoModel()

    def carregar(self):
        self.window.stackedWidget.setCurrentIndex(9)
        dados = self.model.listar()

        total_servicos = len(dados)
        total_valor = sum(s[5] for s in dados if s[5])
        em_andamento = sum(1 for s in dados if s[6] == "Em andamento")
        concluidos = sum(1 for s in dados if s[6] == "Concluído")

        self.window.labelResumoTotalServicos.setText(str(total_servicos))
        self.window.labelResumoTotalValor.setText(f"R$ {total_valor:.2f}")
        self.window.labelResumoEmAndamento.setText(str(em_andamento))
        self.window.labelResumoConcluidos.setText(str(concluidos))

        self.window.tabelaResumo.setRowCount(len(dados))
        self.window.tabelaResumo.verticalHeader().setVisible(False)
        self.window.tabelaResumo.setSelectionBehavior(
            self.window.tabelaResumo.SelectionBehavior.SelectRows
        )
        self.window.tabelaResumo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for linha, s in enumerate(dados):
            self.window.tabelaResumo.setItem(linha, 0, QTableWidgetItem(str(s[0])))
            self.window.tabelaResumo.setItem(linha, 1, QTableWidgetItem(s[1]))
            self.window.tabelaResumo.setItem(linha, 2, QTableWidgetItem(f"{s[2]} {s[3]}"))
            self.window.tabelaResumo.setItem(linha, 3, QTableWidgetItem(s[4]))
            self.window.tabelaResumo.setItem(linha, 4, QTableWidgetItem(f"R$ {s[5]:.2f}"))
            self.window.tabelaResumo.setItem(linha, 5, QTableWidgetItem(s[6]))
            self.window.tabelaResumo.setItem(linha, 6, QTableWidgetItem(str(s[7])))
