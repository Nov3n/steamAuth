# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/noven/Projects/PythonGui/src/ui/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AccountList(object):
    def setupUi(self, AccountList):
        AccountList.setObjectName("AccountList")
        AccountList.resize(350, 500)
        AccountList.setMinimumSize(QtCore.QSize(350, 500))
        self.centralwidget = QtWidgets.QWidget(AccountList)
        self.centralwidget.setObjectName("centralwidget")
        self.accountList = QtWidgets.QScrollArea(self.centralwidget)
        self.accountList.setGeometry(QtCore.QRect(0, 0, 350, 490))
        self.accountList.setMinimumSize(QtCore.QSize(350, 300))
        self.accountList.setMaximumSize(QtCore.QSize(350, 800))
        self.accountList.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        self.accountList.setWidgetResizable(True)
        self.accountList.setObjectName("accountList")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 348, 488))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.accountList.setWidget(self.scrollAreaWidgetContents)
        AccountList.setCentralWidget(self.centralwidget)

        self.retranslateUi(AccountList)
        QtCore.QMetaObject.connectSlotsByName(AccountList)

    def retranslateUi(self, AccountList):
        _translate = QtCore.QCoreApplication.translate
        AccountList.setWindowTitle(_translate("AccountList", "NovenSteamAuth"))
