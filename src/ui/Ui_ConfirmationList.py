# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/noven/Projects/PythonGui/src/ui/ConfirmationList.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConfirmationList(object):
    def setupUi(self, ConfirmationList):
        ConfirmationList.setObjectName("ConfirmationList")
        ConfirmationList.resize(380, 450)
        ConfirmationList.setMinimumSize(QtCore.QSize(380, 450))
        ConfirmationList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        ConfirmationList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        ConfirmationList.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 378, 448))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        ConfirmationList.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(ConfirmationList)
        QtCore.QMetaObject.connectSlotsByName(ConfirmationList)

    def retranslateUi(self, ConfirmationList):
        _translate = QtCore.QCoreApplication.translate
        ConfirmationList.setWindowTitle(_translate("ConfirmationList", "ScrollArea"))