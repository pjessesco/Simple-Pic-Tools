from logging import root

from PyQt5 import QtCore, QtGui, QtWidgets,QtPrintSupport
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenuBar, QWidget
from PyQt5.QtGui import QPixmap
from PIL import ImageQt
from function import *
from dialog import *
from combineDialog import *
from imgWidget import *


class ImageViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super(ImageViewer, self).__init__()

        self.printer = QtPrintSupport.QPrinter()
        self.scaleFactor = 0.0

        selectIcon=QIcon("/Users/jino/SimplePicTool/Simple Pic Tool/select.jpg")

        self.mdiArea=QtWidgets.QMdiArea(self)
        self.mdiArea.setMouseTracking(True)
        self.mdiArea.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.mdiArea.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.mdiArea.setObjectName("mdiArea")
        brush = QtGui.QBrush(QtGui.QColor(100, 191, 191))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.mdiArea.setBackground(brush)
        self.mdiArea.resize(self.width(),self.height())


        self.imgWindow = imgWidget()
        self.imgWindow.setMinimumSize(QtCore.QSize(300, 300))
        self.imgWindow.setMouseTracking(True)
        self.imgWindow.setObjectName("subwindow")
        self.imgWindow.setWindowTitle("Image")


        self.toolWindow=QWidget()
        self.toolWindow.setFixedSize(100,200)
        self.toolWindow.setMaximumSize(101,501)
        self.toolWindow.setWindowTitle("Tools")

        self.selectModeb = QtWidgets.QPushButton(self.toolWindow)
        self.selectModeb.setGeometry(QtCore.QRect(10, 10, 31, 31))
        self.selectModeb.setText("")
        self.selectModeb.setObjectName("selectMode")
        self.selectModeb.setCheckable(True)
        self.selectModeb.setIcon(selectIcon)
        self.selectModeb.setIconSize(self.selectModeb.size())
        self.selectModeb.clicked.connect(self.selectMode)

        self.paintButton = QtWidgets.QPushButton(self.toolWindow)
        self.paintButton.setGeometry(QtCore.QRect(10, 60, 31, 31))
        self.paintButton.setText("")
        self.paintButton.setObjectName("paintButton")
        self.paintButton.clicked.connect(self.paint)

        self.colorButton = QtWidgets.QPushButton(self.toolWindow)
        self.colorButton.setGeometry(QtCore.QRect(0, 110, 91, 61))
        self.colorButton.setText("")
        self.colorButton.setObjectName("colorButton")
        self.colorButton.clicked.connect(self.selectColor)



        self.mdiArea.addSubWindow(self.imgWindow)
        self.mdiArea.addSubWindow(self.toolWindow)

        self.imageLabel = QtWidgets.QLabel(self.imgWindow)
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setSizePolicy(QtWidgets.QSizePolicy.Ignored,
                                      QtWidgets.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)


        self.undoStack=[]
        self.redoStack=[]


        self.setMouseTracking(True)

        self.menuBar=QMenuBar()

        self.createActions()

        self.createMenus()

        self.setWindowTitle("Simple Pic Tool")
        self.resize(1000, 800)


    def selectColor(self):
        a=QtWidgets.QColorDialog()
        self.color=a.getColor()
        p=self.colorButton.palette()
        r=self.colorButton.backgroundRole()
        p.setColor(r,self.color)
        self.colorButton.setPalette(p)
        self.colorButton.setAutoFillBackground(True)


        a=self.color.name()[1:]
        h1, h2, h3 = a[0:2],  a[2:4],  a[4:6]
        a=(int(h1, 16), int(h2, 16), int(h3, 16))


    def paint(self):

        a = self.imgWindow.currentQRubberBand
        if (a != None and a.isVisible()):
            x = a.pos().x()
            y = a.pos().y()
            w = a.width()
            h = a.height()
            del self.redoStack
            self.redoStack = []
            self.undoStack.append((self.image, self.pixmap))
            temp = self.processor.painting(self.image, x, y, w, h,self.color)
            self.image = temp[0]
            self.pixmap = temp[1]
            self.imageLabel.clear()
            self.imageLabel.setPixmap(self.pixmap)





    def open(self):

        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open File",
                QtCore.QDir.currentPath())

        if fileName:

            image = QtGui.QImage(fileName[0])
            if image.isNull():
                QtGui.QMessageBox.information(self, "Simple Pic Tool",
                        "Cannot load %s." % fileName)
                return

            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))

            self.resize(image.width()+300,image.height()+300)
            self.imgWindow.res(image.width(),image.height())


            if(image.width()>1300 or image.height()>600):
                self.imgWindow.setMinimumSize(QtCore.QSize(1200, 800))

            else:
                self.imgWindow.setMinimumSize(image.width(),image.height())
                self.imgWindow.resize(image.width(),image.height())

            self.scaleFactor = 1.0

            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.blackwhiteAct.setEnabled(True)
            self.undoAct.setEnabled(True)
            self.redoAct.setEnabled(True)
            self.rotateAct.setEnabled(True)
            self.symmetryAct.setEnabled(True)
            self.brightAct.setEnabled(True)
            self.shadeAct.setEnabled(True)
            self.blurAct.setEnabled(True)
            self.vividAct.setEnabled(True)
            self.combineAct.setEnabled(True)


            self.updateActions()


            self.image=Image.open(fileName[0])
            self.pixmap=QtGui.QPixmap.fromImage(image)

            self.dl = dialog()
            self.dl.setupUi(self.dl)

            self.processor=processor()  # 프로세서 만들기

            self.pixaccess=self.image.load()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()

    def print_(self):
        dialog = QtGui.QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QtGui.QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), QtCore.Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def save(self):
        self.image.save("a.jpg")

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()
        self.updateActions()

    def brightness(self): # 밝기 clear!
        dl=dialog()
        dl.setupUi(dl)
        if(dl.exec_()):
            param=dl.getValue()*2.55
            del self.redoStack
            self.redoStack = []
            self.undoStack.append((self.image, self.pixmap))
            temp = self.processor.brightness(self.image,param)
            self.image = temp[0]
            self.pixmap = temp[1]
            self.imageLabel.clear()
            self.imageLabel.setPixmap(self.pixmap)
        pass

    def shade(self): # 명암 clear!
        dl = dialog()
        dl.setupUi(dl)
        if (dl.exec_()):
            if(dl.getValue()<0):
                param=(100+dl.getValue())/100
            else:
                param=100/(100-dl.getValue()/2)
            del self.redoStack
            self.redoStack = []
            self.undoStack.append((self.image, self.pixmap))
            temp = self.processor.shade(self.image,param)
            self.image = temp[0]
            self.pixmap = temp[1]
            self.imageLabel.clear()
            self.imageLabel.setPixmap(self.pixmap)


    def blackwhite(self): # 흑백 clear!

        del self.redoStack
        self.redoStack=[]
        self.undoStack.append((self.image,self.pixmap))
        temp = self.processor.blackwhite(self.image)
        self.image=temp[0]
        self.pixmap=temp[1]
        self.imageLabel.clear()
        self.imageLabel.setPixmap(self.pixmap)


    def combine(self): # 합성 TODO
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open File",
                                                         QtCore.QDir.currentPath())
        if fileName:
            cdl=combineDialog()
            cdl.setupUi(cdl,self.image,Image.open(fileName[0]))
            if(cdl.exec_()):
                del self.redoStack
                self.redoStack = []
                self.undoStack.append((self.image,self.pixmap))
                temp=cdl.getImage()
                self.image = temp[0]
                self.pixmap = temp[1]
                self.imageLabel.clear()
                self.imageLabel.setPixmap(self.pixmap)
                del cdl
        pass

    def blur(self): # 흐리게
        del self.redoStack
        self.redoStack = []
        self.undoStack.append((self.image,self.pixmap))
        temp=self.processor.blur(self.image)
        self.image=temp[0]
        self.pixmap=temp[1]
        self.imageLabel.clear()
        self.imageLabel.setPixmap(self.pixmap)
        pass

    def vivid(self): # 선명하게
        del self.redoStack
        self.redoStack = []
        self.undoStack.append((self.image, self.pixmap))
        temp = self.processor.vivid(self.image)
        self.image = temp[0]
        self.pixmap = temp[1]
        self.imageLabel.clear()
        self.imageLabel.setPixmap(self.pixmap)

    def rotate(self): # 회전
        pass

    def symmetry(self): # 대칭
        pass

    def smile(self):
        a=self.imgWindow.currentQRubberBand
        if (a!=None and a.isVisible()):
            x=a.pos().x()
            y=a.pos().y()
            w=a.width()
            h=a.height()
            del self.redoStack
            self.redoStack = []
            self.undoStack.append((self.image, self.pixmap))
            temp = self.processor.smile(self.image,x,y,w,h)
            self.image = temp[0]
            self.pixmap = temp[1]
            self.imageLabel.clear()
            self.imageLabel.setPixmap(self.pixmap)

    def selectMode(self):
        self.imgWindow.selectMode=self.selectModeb.isChecked()
        print(self.imgWindow.selectMode)

    def undo(self):
        if(len(self.undoStack)>0):
            self.redoStack.append((self.image,self.pixmap))
            pop=self.undoStack.pop()
            self.image=pop[0]
            self.pixmap=pop[1]
            self.imageLabel.clear()
            self.imageLabel.setPixmap(self.pixmap)
        pass

    def redo(self):
        if(len(self.redoStack)>0):
            self.undoStack.append((self.image,self.pixmap))
            pop=self.redoStack.pop()
            self.image=pop[0]
            self.pixmap=pop[1]
            self.imageLabel.clear()
            self.imageLabel.setPixmap(self.pixmap)

    def about(self):
        QtWidgets.QMessageBox.about(self, "About Simple Pic Tool",
                "sdfsdf")

    def createActions(self):

        # 파일 액션

        self.openAct = QtWidgets.QAction("&열기...", self, shortcut="Ctrl+O",
                triggered=self.open)

        self.printAct = QtWidgets.QAction("&인쇄하기...", self, shortcut="Ctrl+P",
                enabled=False, triggered=self.print_)

        self.saveAct=QtWidgets.QAction("&저장", self, shortcut="Ctrl+S",
                enabled=True, triggered=self.save)


        self.zoomInAct = QtWidgets.QAction("확대 (25%)", self,
                shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)

        self.zoomOutAct = QtWidgets.QAction("축소 (25%)", self,
                shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)

        self.normalSizeAct = QtWidgets.QAction("&원본 크기", self,
                 enabled=False, triggered=self.normalSize)

        self.fitToWindowAct = QtWidgets.QAction("&창에 맞추기", self,
                enabled=False, checkable=True, shortcut="Ctrl+F",
                triggered=self.fitToWindow)

        #도움말 액션...왜 안생기고 Python 메뉴안으로 들어가지?

        self.aboutAct = QtWidgets.QAction("&about", self, triggered=self.about)

        # 필터 액션
        #  흑백 합성 흐리게 선명하게
        # brightness, shade, blackwhite, combine, blur, aasdf(선명), rotate, symmetry

        self.blackwhiteAct=QtWidgets.QAction("흑백 필터",self,triggered=self.blackwhite,enabled=False)
        self.combineAct=QtWidgets.QAction("합성",self,triggered=self.combine,enabled=False)
        self.blurAct=QtWidgets.QAction("흐리게",self,triggered=self.blur,enabled=False)
        self.vividAct=QtWidgets.QAction("선명하게",self,triggered=self.vivid,enabled=False)

        # 편집 액션    입력취소, 다시실행

        self.undoAct=QtWidgets.QAction("입력 취소",self,shortcut="Ctrl+Z",triggered=self.undo,enabled=False)
        self.redoAct = QtWidgets.QAction("다시 실행", self,shortcut="Ctrl+Shift+Z",triggered=self.redo, enabled=False)

        # 이미지 액션   회전, 뒤집기

        self.rotateAct=QtWidgets.QAction("회전",self,triggered=self.rotate,enabled=False)
        self.symmetryAct = QtWidgets.QAction("뒤집기", self, triggered=self.symmetry, enabled=False)

        # 조정 액션    밝기, 명암

        self.brightAct=QtWidgets.QAction("밝기",self,triggered=self.brightness,enabled=False)
        self.shadeAct=QtWidgets.QAction("명암",self,triggered=self.shade,enabled=False)

        # 스티커
        self.smileAct=QtWidgets.QAction("스마일",self,triggered=self.smile)

    def createMenus(self):
        self.fileMenu = QtWidgets.QMenu("&파일", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addAction(self.saveAct)


        self.fixMenu = QtWidgets.QMenu("&편집", self) # 입력취소, 다시실행
        self.fixMenu.addAction(self.undoAct)
        self.fixMenu.addAction(self.redoAct)


        self.imageMenu = QtWidgets.QMenu("&이미지", self) # 회전, 뒤집기
        self.imageMenu.addAction(self.rotateAct)
        self.imageMenu.addAction(self.symmetryAct)

        self.adjustMenu = QtWidgets.QMenu("&조정", self) # 밝기, 명암
        self.adjustMenu.addAction(self.brightAct)
        self.adjustMenu.addAction(self.shadeAct)


        self.filterMenu=QtWidgets.QMenu("&필터",self)
        self.filterMenu.addAction(self.blackwhiteAct)
        self.filterMenu.addAction(self.blurAct)
        self.filterMenu.addAction(self.vividAct)
        self.filterMenu.addAction(self.combineAct)

        self.stickerMenu = QtWidgets.QMenu("&스티커", self)
        self.stickerMenu.addAction(self.smileAct)

        self.viewMenu = QtWidgets.QMenu("&보기", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.helpMenu = QtWidgets.QMenu("&도움말", self)
        self.helpMenu.addAction(self.aboutAct)


        self.menuBar.addMenu(self.fileMenu)
        self.menuBar.addMenu(self.fixMenu)
        self.menuBar.addMenu(self.imageMenu)
        self.menuBar.addMenu(self.adjustMenu)
        self.menuBar.addMenu(self.filterMenu)
        self.menuBar.addMenu(self.viewMenu)
        self.menuBar.addMenu(self.helpMenu)
        self.menuBar.addMenu(self.stickerMenu)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                                + ((factor - 1) * scrollBar.pageStep()/2)))

    def resizeEvent(self, QResizeEvent):
        self.mdiArea.resize(QResizeEvent.size())



