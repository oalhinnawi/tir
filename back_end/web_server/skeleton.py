# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'email_gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(523, 432)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 0, 251, 61))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.subreddit_input = QtWidgets.QLineEdit(Form)
        self.subreddit_input.setGeometry(QtCore.QRect(10, 70, 411, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.subreddit_input.setFont(font)
        self.subreddit_input.setObjectName("subreddit_input")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 150, 391, 61))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.dateEdit = QtWidgets.QDateEdit(Form)
        self.dateEdit.setGeometry(QtCore.QRect(10, 210, 251, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.dateEdit.setFont(font)
        self.dateEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2017, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit.setObjectName("dateEdit")
        self.start_analysis_button = QtWidgets.QPushButton(Form)
        self.start_analysis_button.setGeometry(QtCore.QRect(10, 300, 341, 81))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.start_analysis_button.setFont(font)
        self.start_analysis_button.setObjectName("start_analysis_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "SUBREDDIT:"))
        self.subreddit_input.setText(_translate("Form", "NBA"))
        self.label_2.setText(_translate("Form", "DATE:"))
        self.start_analysis_button.setText(_translate("Form", "Get Topic Analysis"))
