from PyQt5 import QtCore, QtGui, QtWidgets,QtPrintSupport


class imgWidget(QtWidgets.QWidget):

    def __init__(self):
        super(imgWidget,self).__init__()
        self.currentQRubberBand = None
        self.selectMode=False


    def res(self,a,b):
        self.resize(a,b)

    def mousePressEvent(self, eventQMouseEvent):

        if(self.selectMode):

            if(self.currentQRubberBand!=None):
                self.currentQRubberBand.hide()
                del self.currentQRubberBand
            self.originQPoint = eventQMouseEvent.pos()
            self.currentQRubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)

            self.currentQRubberBand.setGeometry(QtCore.QRect(self.originQPoint, QtCore.QSize()))


    def mouseMoveEvent(self, eventQMouseEvent):

        if (self.selectMode):

            if(self.currentQRubberBand!=None):

                x=eventQMouseEvent.pos().x()
                y=eventQMouseEvent.pos().y()

                # if()

                self.currentQRubberBand.setGeometry(QtCore.QRect(self.originQPoint, eventQMouseEvent.pos()).normalized())
                self.currentQRubberBand.show()


    def mouseReleaseEvent(self, eventQMouseEvent):
        if (self.selectMode):

            currentQRect = self.currentQRubberBand.geometry()


