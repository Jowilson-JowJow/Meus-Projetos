import os
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QMessageBox
from models.usuario_model import UsuarioModel
from controllers.home_controller import HomeController

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIEW_DIR = os.path.join(BASE_DIR, "..", "views")

class LoginController:

    def __init__(self):
        loader = QUiLoader()
        file = QFile(os.path.join(VIEW_DIR, "login.ui"))
        file.open(QFile.ReadOnly)
        self.window = loader.load(file)
        file.close()

        self.model = UsuarioModel()

        self.window.btnLoginEntrar.clicked.connect(self.login)

    def login(self):
        email = self.window.inputLoginEmail.text()
        senha = self.window.inputLoginSenha.text()

        if not email or not senha:
            QMessageBox.warning(self.window, "Atenção", "Preencha o e-mail e a senha!")
            return

        usuario = self.model.validar_login(email, senha)

        if usuario:
            self.abrir_home()
        else:
            QMessageBox.critical(self.window, "Erro", "E-mail ou senha incorretos!")

    def abrir_home(self):
        self.home = HomeController()
        self.home.show()
        self.window.close()

    def show(self):
        self.window.show()
