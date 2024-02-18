from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit, QTextEdit, QProgressBar, QLabel
import sys
from Core import core as mycore


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setFixedSize(700, 150)
        uic.loadUi('gss.ui', self)  # Load the .ui file

        # define widgets
        self.btn = self.findChild(QPushButton, "btn")
        self.inputName = self.findChild(QLineEdit, "inputName")
        self.inputURL = self.findChild(QTextEdit, "inputURL")
        self.progressBar = self.findChild(QProgressBar, "progressbar")
        self.label = self.findChild(QLabel, "label")

        self.setWindowTitle("GSS")

        # adding functions
        self.btn.clicked.connect(self.myfunction)

    def is_url(self, url):
        return "scholar.google.com/citations?view_op=search_authors" in url

    def myfunction(self):
        myurl = str(self.inputURL.toPlainText())
        myname = str(self.inputName.text())
        print(myurl, " ------------ ", myname)
        if self.is_url(myurl):
            tmpdata = mycore.scrape_all_pages(myurl)
            nbrprofiles = tmpdata[1]
            mycore.convert_2_json(tmpdata, myname)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()

    app.exec()


main()
