from penstate import PenState
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

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
        center_x = self.circle_start_x
        center_y =  self.circle_start_y
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
