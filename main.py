import random
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from enum import Enum


COLORS = [
    '#000000',  # Negru
    '#FFFFFF',  # Alb
    '#808080',  # Gri
    '#D32F2F',  # Roșu deschis
    '#1976D2',  # Albastru
    '#388E3C',  # Verde
    '#FBC02D',  # Galben deschis
    '#7B1FA2',  # Mov deschis
    '#E64A19',  # Portocaliu închis
    '#0288D1',  # Albastru deschis
    '#689F38',  # Verde închis
    '#C2185B',  # Roz
    '#512DA8',  # Mov închis
    '#FFA000',  # Portocaliu deschis
    '#00796B',  # Verde închis
    '#FF5722',  # Roșu intens
    '#689F38',  # Verde închis
    '#D84315',  # Portocaliu închis
    '#303F9F',  # Albastru închis
    '#8BC34A',  # Verde deschis
    '#FBC02D',  # Galben deschis
    '#8D6E63',  # Maro
    '#9E9E9E',  # Gri
    '#F57C00',  # Portocaliu
    '#673AB7',  # Violet
    '#3E2723',  # Maro închis
    '#607D8B',  # Gri deschis
    '#4CAF50',  # Verde deschis
    '#FFD600',  # Galben intens
    '#01579B'   # Albastru închis
]


class PenState(Enum):
    NORMAL = 1
    SPRAY = 2
    BRUSH = 3
    FILL = 4
    RECTANGLE = 5
    CIRCLE = 6

class Canvas(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        pixmap = QtGui.QPixmap(1800, 1000)
        pixmap.fill(Qt.white)
        self.setPixmap(pixmap)
        self.penState = PenState.NORMAL
        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor('#000000')
        self.pen_width = 10
        self.slider = 10
        self.rectangle_start_x, self.rectangle_start_y = None, None
        self.circle_start_x, self.circle_start_y = None, None
        self.isDrawingRect = False
        self.isDrawingCircle = False

    def set_pen_color(self, c):
        self.pen_color = QtGui.QColor(c)

    def drawSpray(self):
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(1)
        p.setColor(self.pen_color)
        painter.setPen(p)

        for _ in range(self.pen_width*3):
            xo = round(random.gauss(0, 10))
            yo = round(random.gauss(0, 10))
            painter.drawPoint(self.last_x + xo, self.last_y + yo)

        painter.end()
        self.update()

    def drawNormal(self,e):
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(self.pen_width)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.update()

    def drawBrush(self, e):
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        initial_width = self.pen_width

        #Distanța euclidiană este calculată folosind formula pentru distanța în planul cartezian între două puncte
        #cu cat cursorul se misca mai repede cu atat grosimea pensulei va fi mai mica
        dist = max(1, (self.last_x - e.x()) ** 2 + (self.last_y - e.y()) ** 2)
        new_width = initial_width / (dist ** 0.4)

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

    def drawFill(self, e):
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setColor(self.pen_color)
        painter.setPen(p)

        painter.fillRect(self.rect(), self.pen_color)
        painter.end()
        self.update()

    def drawRectangle(self, start_x, start_y, end_x, end_y):
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(self.pen_width)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setOpacity(1.0)
        painter.drawRect(start_x, start_y, end_x - start_x, end_y - start_y)
        painter.end()
        self.update()

    def drawCircle(self, x, y):
        pixmap = self.pixmap()
        painter = QtGui.QPainter(pixmap)
        p = painter.pen()
        p.setWidth(self.pen_width)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setOpacity(1.0)
        radius = max(abs(x - self.circle_start_x), abs(y - self.circle_start_y))
        center_x = (x + self.circle_start_x) // 2
        center_y = (y + self.circle_start_y) // 2
        painter.drawEllipse(center_x - radius, center_y - radius, 2 * radius, 2 * radius)
        painter.end()
        self.update()
        

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0:
            self.pen_width += 1
        else:
            self.pen_width -= 1
        self.pen_width = max(1, min(self.pen_width, 35))

    def mousePressEvent(self, e):
        if self.penState == PenState.FILL:
            self.drawFill(e)
        elif self.penState == PenState.RECTANGLE:
            self.is_drawing_rectangle = True
            self.rectangle_start_x = e.x()
            self.rectangle_start_y = e.y()
        elif self.penState == PenState.CIRCLE:  
            self.isDrawingCircle = True
            self.circle_start_x = e.x()
            self.circle_start_y = e.y()

    def mouseMoveEvent(self, e):
        if self.last_x is None:
            self.last_x = e.x()
            self.last_y = e.y()
            return

        if(self.penState == PenState.NORMAL):
            self.drawNormal(e)
        elif(self.penState == PenState.SPRAY):
            self.drawSpray()
        elif(self.penState == PenState.BRUSH):
            self.drawBrush(e)
        elif(self.penState == PenState.RECTANGLE):
            self.drawRectangle(self.rectangle_start_x, self.rectangle_start_y, e.x(), e.y())
        elif self.isDrawingCircle:  
            self.drawCircle(e.x(), e.y())

        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        if self.isDrawingRect:
            self.isDrawingRect = False
            self.drawRectangle(self.rectangle_start_x, self.rectangle_start_y, e.x(), e.y())
        elif self.isDrawingCircle:  
            self.isDrawingCircle = False
            self.drawCircle(e.x(), e.y())
            self.last_x = None
            self.last_y = None
        else:
            self.last_x = None
            self.last_y = None


class Menu(QtWidgets.QFrame):
    def __init__(self,  canvas):
        super().__init__()
        self.setStyleSheet("background-color: #494d5f")

        layout = QtWidgets.QGridLayout(self)
        self.canvas = canvas

        sizeSlider = QtWidgets.QSlider(Qt.Horizontal)
        sizeSlider.setRange(1,35)
        sizeSlider.setFixedSize(200, sizeSlider.sizeHint().height())
        layout.addWidget(sizeSlider,3,0,1,2,Qt.AlignmentFlag.AlignCenter)
        sizeSlider.setStyleSheet(
            """
            QSlider::groove:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0078d7, stop:1 #00bfff);
                border: 1px solid #0078d7;
                height: 8px;
                border-radius: 4px;
            }

            QSlider::handle:horizontal {
                background: #00bfff;
                border: 1px solid #0078d7;
                width: 16px;
                height: 16px;
                margin: -8px 0px; 
                border-radius: 8px;
            }

            QSlider::add-page:horizontal {
                background: #0078d7;
                border: 1px solid #0078d7;
                border-radius: 4px;
            }
            """
        )

        buttonSpray = self.create_button("./icons/spray.png", "")
        layout.addWidget(buttonSpray, 0, 0)

        buttonBrush = self.create_button('./icons/brush.png', "")
        layout.addWidget(buttonBrush, 0, 1)

        buttonPen = self.create_button('./icons/pencil.png', "")
        layout.addWidget(buttonPen, 1, 0)

        buttonFill = self.create_button('./icons/fill.png', "")
        layout.addWidget(buttonFill, 1, 1)

        buttonRectangle = self.create_button('./icons/square.png', "")
        layout.addWidget(buttonRectangle, 2, 0)

        buttonCircle = self.create_button('./icons/circle.png', "")
        layout.addWidget(buttonCircle, 2, 1)

        buttonBrush.clicked.connect(self.onBrush)
        buttonSpray.clicked.connect(self.onSpray)
        buttonPen.clicked.connect(self.onPen)
        buttonFill.clicked.connect(self.onFill)
        buttonRectangle.clicked.connect(self.onRectangle)
        buttonCircle.clicked.connect(self.onCircle)
        sizeSlider.valueChanged.connect(self.setSize)

    def onSpray(self):
        self.canvas.penState = PenState.SPRAY
    def onBrush(self):
        self.canvas.penState = PenState.BRUSH
    def onPen(self):
        self.canvas.penState = PenState.NORMAL
    def onFill(self):
        self.canvas.penState = PenState.FILL
    def setSize(self,value):
        self.canvas.pen_width = value
    def onRectangle(self):
        self.canvas.penState = PenState.RECTANGLE
    def onCircle(self):
        self.canvas.penState = PenState.CIRCLE

    def create_button(self,icon_path, text):
        button = QtWidgets.QPushButton()
        button.setIconSize(QtCore.QSize(40, 40))  
        button.setIcon(QtGui.QIcon(icon_path))
        button.setText(text)
        button.setStyleSheet(
            "QPushButton {"
            "background-color: #333;"
            "color: white;"
            "padding: 10px;"
            "border: 2px solid #555;"  
            "border-radius: 15px;"  
            "}"
            "QPushButton:hover {"
            "background-color: #555;"  
            "}"
        )
        return button


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