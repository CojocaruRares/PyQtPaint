from penstate import PenState
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

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