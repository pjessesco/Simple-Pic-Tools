# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class dialog(QtWidgets.QDialog):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(230, 144)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 100, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.paramSlider = QtWidgets.QSlider(Dialog)
        self.paramSlider.setGeometry(QtCore.QRect(30, 70, 160, 22))
        self.paramSlider.setMinimumSize(QtCore.QSize(160, 0))
        self.paramSlider.setMaximumSize(QtCore.QSize(160, 16777215))
        self.paramSlider.setMinimum(-100)
        self.paramSlider.setMaximum(100)
        self.paramSlider.setProperty("value", 0)
        self.paramSlider.setOrientation(QtCore.Qt.Horizontal)
        self.paramSlider.setObjectName("paramSlider")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(80, 20, 71, 31))
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label.setLineWidth(0)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.paramSlider.sliderMoved['int'].connect(self.label.setNum)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "0"))

    def getValue(self):
        return self.paramSlider.value()

