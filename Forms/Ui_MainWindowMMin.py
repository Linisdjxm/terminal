# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\MainWindowMMin.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindowMMin(object):
    def setupUi(self, MainWindowMMin):
        MainWindowMMin.setObjectName("MainWindowMMin")
        MainWindowMMin.resize(988, 648)
        self.label = QtWidgets.QLabel(MainWindowMMin)
        self.label.setGeometry(QtCore.QRect(-5, 8, 1001, 641))
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(MainWindowMMin)
        self.pushButton.setGeometry(QtCore.QRect(30, 520, 161, 101))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(MainWindowMMin)
        self.pushButton_2.setGeometry(QtCore.QRect(790, 510, 161, 101))
        self.pushButton_2.setObjectName("pushButton_2")
        self.checkBox = QtWidgets.QCheckBox(MainWindowMMin)
        self.checkBox.setGeometry(QtCore.QRect(20, 30, 138, 28))
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.comboBox = QtWidgets.QComboBox(MainWindowMMin)
        self.comboBox.setGeometry(QtCore.QRect(40, 130, 128, 30))
        self.comboBox.setObjectName("comboBox")
        self.label_2 = QtWidgets.QLabel(MainWindowMMin)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 171, 24))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(MainWindowMMin)
        QtCore.QMetaObject.connectSlotsByName(MainWindowMMin)

    def retranslateUi(self, MainWindowMMin):
        _translate = QtCore.QCoreApplication.translate
        MainWindowMMin.setWindowTitle(_translate("MainWindowMMin", "Form"))
        self.pushButton.setText(_translate("MainWindowMMin", "Prev"))
        self.pushButton_2.setText(_translate("MainWindowMMin", "Next"))
        self.checkBox.setText(_translate("MainWindowMMin", "Camera"))
        self.label_2.setText(_translate("MainWindowMMin", "Image Quality"))

