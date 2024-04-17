from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow

from Snake import Snake


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setCentralWidget(Snake())

        self.setWindowTitle("Snake")

        #self.setStyleSheet("background-color: black;")
