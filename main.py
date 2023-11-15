import random
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from colors import COLORS
from menu import Menu
from canvas import Canvas


class QPaletteButton(QtWidgets.QPushButton):

    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QtCore.QSize(24,24))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.canvas = Canvas()
        self.menu = Menu( self.canvas)
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        widget.setLayout(layout)
        layout.addWidget(self.menu)
        layout.addWidget(self.canvas)
        palette = QtWidgets.QVBoxLayout()
        self.add_palette_buttons(palette)
        layout.addLayout(palette)
        self.setCentralWidget(widget)

    def add_palette_buttons(self, layout):
        for c in COLORS:
            b = QPaletteButton(c)
            b.pressed.connect(lambda c=c: self.canvas.set_pen_color(c))
            layout.addWidget(b)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.showMaximized()
app.exec_()