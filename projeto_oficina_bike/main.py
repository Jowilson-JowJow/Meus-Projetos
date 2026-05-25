import sys
import os
from PySide6.QtWidgets import QApplication
from controllers.login_controller import LoginController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginController()
    login.show()
    sys.exit(app.exec())
