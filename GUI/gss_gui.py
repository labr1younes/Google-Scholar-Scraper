from PyQt5 import QtWidgets ,uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import sys


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setFixedSize(700, 150)
        uic.loadUi('gss.ui', self)  # Load the .ui file


def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()

    app.exec()


main()
