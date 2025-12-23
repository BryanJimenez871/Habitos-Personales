import sys
from PySide6.QtWidgets import QApplication
from Interfaz.VentanaPrincipal import VentanaPrincipal

if __name__ == '__main__':
    app = QApplication([])
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec())


