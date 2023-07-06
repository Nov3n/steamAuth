# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect_me.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
#导入程序运行必须模块
import sys
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from src.ui.Ui_MainWindow import Ui_AccountList
from PyQt5.QtCore import Qt
import json
from src.py.MyBlocks import MyAccountBlock
from src.ui.Ui_AccountBlock import Ui_AccountBlock




# conf设置成多个steam_account的数组
class MyMainWindow(QMainWindow, Ui_AccountList):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.SteamClientList = []
        # 读取steam信息
        steam_conf_list = json.load(open("./conf/test.json", "r", encoding="utf8"))
        for i in range(0, len(steam_conf_list)):
            # self.SteamClientList.append(MySteamClient(steam_conf_list[i]))
            self.add_steam_client(steam_conf_list[i])
            pass
    
    def add_steam_client(self, steam_conf):
        if not self.scrollArea.layout():
            # 需要添加布局管理器之后才可以使用布局管理器添加子控件
            accountListLayout = QVBoxLayout()
            self.scrollArea.setLayout(accountListLayout)
        ui_steam_account = MyAccountBlock(steam_conf)
        self.scrollArea.layout().addWidget(ui_steam_account)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    #程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())