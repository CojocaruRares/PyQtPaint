import random
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from enum import Enum


COLORS = [
'#000000', '#141923', '#414168', '#3a7fa7', '#35e3e3', '#8fd970', '#5ebb49',
'#458352', '#dcd37b', '#fffee5', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b',
'#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff',
]

class PenState(Enum):
    NORMAL = 1
    SPRAY = 2
    BRUSH = 3

class Canvas(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        pixmap = QtGui.QPixmap(1000, 700)
        pixmap.fill(Qt.white)
        self.setPixmap(pixmap)
        self.penState = PenState.NORMAL
        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor('#000000')

    def set_pen_color(self, c):
        self.pen_color = QtGui.QColor(c)

    def drawSpray(self,e):
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(1)  # Reducem lățimea liniei pentru un efect mai fin
        p.setColor(self.pen_color)
        painter.setPen(p)

        for _ in range(100):
            xo = round(random.gauss(0, 10))
            yo = round(random.gauss(0, 10))
            painter.drawPoint(self.last_x + xo, self.last_y + yo)

        painter.end()
        self.update()

    def drawNormal(self,e):
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(4)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.update()

    def drawBrush(self, e):
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        initial_width = 20

        #Distanța euclidiană este calculată folosind formula pentru distanța în planul cartezian între două puncte
        #cu cat cursorul se misca mai repede cu atat grosimea pensulei va fi mai mica
        dist = max(1, (self.last_x - e.x()) ** 2 + (self.last_y - e.y()) ** 2)
        new_width = initial_width / (dist ** 0.3)

        p.setWidth(int(new_width))
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        opacity = 0.5
        painter.setOpacity(opacity)
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.update()

        self.last_x = e.x()
        self.last_y = e.y()

    def mouseMoveEvent(self, e):
        if self.last_x is None:
            self.last_x = e.x()
            self.last_y = e.y()
            return

        if(self.penState == PenState.NORMAL):
            self.drawNormal(e)
        elif(self.penState == PenState.SPRAY):
            self.drawSpray(e)
        elif(self.penState == PenState.BRUSH):
            self.drawBrush(e)

        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None


class Menu(QtWidgets.QFrame):
    def __init__(self, w, h, canvas):
        super().__init__()
        self.setStyleSheet("background-color: #494d5f")

        self.setFixedSize(w, h)

        layout = QtWidgets.QGridLayout(self)
        self.canvas = canvas

        sizeSlider = QtWidgets.QSlider(Qt.Horizontal)
        sizeSlider.setRange(5,35)
        sizeSlider.setFixedSize(200, sizeSlider.sizeHint().height())
        layout.addWidget(sizeSlider,2,0,1,2,Qt.AlignmentFlag.AlignCenter)

        buttonSpray = QtWidgets.QPushButton("Spray")
        buttonSpray.setStyleSheet("background-color: #333; color: white; padding: 5px 10px")
        layout.addWidget(buttonSpray, 0, 0)

        buttonBrush = QtWidgets.QPushButton("Brush")
        buttonBrush.setStyleSheet("background-color: #333; color: white; padding: 5px 10px")
        layout.addWidget(buttonBrush, 0, 1)

        buttonPen = QtWidgets.QPushButton("Pen")
        buttonPen.setStyleSheet("background-color: #333; color: white; padding: 5px 10px")
        layout.addWidget(buttonPen, 1, 0)

        buttonEraser = QtWidgets.QPushButton("Eraser")
        buttonEraser.setStyleSheet("background-color: #333; color: white; padding: 5px 10px")
        layout.addWidget(buttonEraser, 1, 1)

        buttonBrush.clicked.connect(self.onBrush)
        buttonSpray.clicked.connect(self.onSpray)
        buttonPen.clicked.connect(self.onPen)

    def onSpray(self):
        self.canvas.penState = PenState.SPRAY
    def onBrush(self):
        self.canvas.penState = PenState.BRUSH
    def onPen(self):
        self.canvas.penState = PenState.NORMAL


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
        self.menu = Menu(300,677, self.canvas)

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
window.setFixedSize(1300,700)
window.show()
app.exec_()