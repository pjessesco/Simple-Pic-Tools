# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'combineDialog.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image,ImageQt
from PyQt5.QtGui import QPixmap

class combineDialog(QtWidgets.QDialog):

    def setupUi(self, combineDialog,imgA,imgB):

        self.pixmapArray = [None] * 102
        self.imgA = imgA
        self.imgB = imgB.resize((imgA.width,imgA.height),Image.ANTIALIAS)

        combineDialog.setObjectName("combineDialog")
        combineDialog.resize(imgA.width+40, imgA.height+100)
        self.buttonBox = QtWidgets.QDialogButtonBox(combineDialog)
        self.buttonBox.setGeometry(QtCore.QRect(220, 420, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(combineDialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 551, 381))
        self.label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label.setText("")
        self.label.setObjectName("label")
        self.label.resize(imgA.width,imgA.height)
        self.horizontalSlider = QtWidgets.QSlider(combineDialog)
        self.horizontalSlider.setGeometry(QtCore.QRect(40, 420, 341, 22))
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setSliderPosition(50)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")

        self.retranslateUi(combineDialog)
        self.buttonBox.accepted.connect(combineDialog.accept)
        self.buttonBox.rejected.connect(combineDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(combineDialog)

        self.horizontalSlider.sliderMoved['int'].connect(self.adjustPixmap)

        self.pixmapArray[50] = \
            QPixmap.fromImage(ImageQt.ImageQt(Image.blend(self.imgA, self.imgB, float(50) / 100)))

        self.pixmapArray[50].detach()

        self.label.setPixmap(self.pixmapArray[50])
        self.slideValue=50



    def retranslateUi(self, combineDialog):
        _translate = QtCore.QCoreApplication.translate
        combineDialog.setWindowTitle(_translate("combineDialog", "Dialog"))

    def adjustPixmap(self):

        self.slideValue=self.horizontalSlider.value()

        if(self.pixmapArray[self.slideValue]==None):
            self.pixmapArray[self.slideValue]=\
                QPixmap.fromImage(ImageQt.ImageQt(Image.blend(self.imgA,self.imgB,float(self.slideValue)/100)))

            self.pixmapArray[self.slideValue].detach()

        self.label.setPixmap(self.pixmapArray[self.slideValue])


    def getImage(self):

        img=Image.blend(self.imgA,self.imgB,float(self.slideValue)/100)
        pix=QPixmap.fromImage(ImageQt.ImageQt(img))
        pix.detach()

        return (img,pix)

        pass