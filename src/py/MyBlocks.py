from ..ui.Ui_AccountBlock import Ui_AccountBlock as AccountBlock
from ..ui.Ui_MainWindow import Ui_AccountList
from ..ui.Ui_ConfirmationBlock import Ui_ConfirmationBlock as ConfirmBlock
from ..ui.Ui_ConfirmationList import Ui_ConfirmationList as ConfirmList
from ..py.MySteamClient import MySteamClient, MyConfirmation
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests, time, json


# conf设置成多个steam_account的数组
class MyMainWindow(QMainWindow, Ui_AccountList):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.__accountBlockList = []
        self.__inner_widget = None
        self.__inner_widget_layout = None
        # 读取steam信息
        steam_conf_list = json.load(open("./conf/test.json", "r", encoding="utf8"))
        for i in range(0, len(steam_conf_list)):
            self.add_steam_client(steam_conf_list[i])
            time.sleep(5)
            pass

    def add_steam_client(self, steam_conf):
        if not self.__inner_widget:
            self.__inner_widget = QWidget()
            self.__inner_widget_layout = QVBoxLayout()
            self.__inner_widget.setLayout(self.__inner_widget_layout)
        ui_steam_account = MyAccountBlock(steam_conf)
        self.__inner_widget_layout.addWidget(ui_steam_account)
        self.__accountBlockList.append(ui_steam_account)
        self.accountList.setWidget(self.__inner_widget)
        self.accountList.show()

    def closeEvent(self, a0: QCloseEvent) -> None:
        for accountBlock in self.__accountBlockList:
            accountBlock.waitExit()
        print("关闭窗口")


class MyConfirmationList(QScrollArea, ConfirmList):
    def __init__(self, parent=None):
        super(MyConfirmationList, self).__init__(parent)
        self.setupUi(self)
        self.__inner_widget = QWidget()
        self.__inner_widget_layout = QVBoxLayout()
        self.__inner_widget.setLayout(self.__inner_widget_layout)

    def showConfirmations(self, confirmatios):
        self.__confirmations = confirmatios
        for confirmation in confirmatios:
            self.__inner_widget_layout.addWidget(confirmation)
        self.setWidget(self.__inner_widget)
        self.show()


class MyConfirmBlock(QWidget, ConfirmBlock):
    def __init__(self, confirmation, parent=None):
        super(MyConfirmBlock, self).__init__(parent)
        self.setupUi(self)
        self.confirmation = confirmation
        self.confirm.clicked.connect(self.accept)
        self.cancel.clicked.connect(self.reject)
        self.ui()

    def ui(self):
        # req = requests.get(self.confirmation.get_parter_avatar())
        req = requests.get(self.confirmation.get_parter_avatar())
        photo = QPixmap()
        photo.loadFromData(req.content)

        label = QLabel()
        label.setPixmap(photo)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.registerDate.setText(self.confirmation.get_parter_register_date())
        self.avatar.setLayout(layout)

    def accept(self):
        if self.__accept:
            try:
                rsp = self.__accept(self.confirmation.get_trade_offer())
                if rsp.get("success", False):
                    self.show_res(0)
                else:
                    self.show_res(2)
            except:
                self.show_res(2)
        pass

    def reject(self):
        if self.__reject:
            try:
                rsp = self.__reject(self.confirmation.get_trade_offer())
                if rsp.get("tradeofferid", False):
                    self.show_res(1)
                else:
                    self.show_res(3)
            except:
                self.show_res(3)
        pass

    # res: 0-确认成功, 1-取消成功, 2-确认失败, 3-取消失败
    def show_res(self, res):
        res_str_list = ["确认成功", "取消成功", "确认失败", "取消失败"]
        self.confirm.deleteLater()
        self.cancel.deleteLater()
        label = QLabel()
        res_str = res_str_list[res]
        label.setText(res_str)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.confirmRes.setLayout(layout)

    def _set_accept(self, accept_func):
        self.__accept = accept_func

    def _set_reject(self, reject_func):
        self.__reject = reject_func


class MyCodeGenerateWorker(QObject):
    # 实际上应该对外提供接口, 传入槽函数进行内部connect
    __sig_code_generated = pyqtSignal(str)
    __sig_finish = pyqtSignal()
    __thread_run = True

    def __init__(self, steam_client):
        super(MyCodeGenerateWorker, self).__init__()
        self.__thread_run = True
        self.__steam_client = steam_client
        self.__is_running = False

    def run(self):
        self.__is_running = True
        while self.__thread_run:
            self.__sig_code_generated.emit(self.__steam_client.generate_code())
            sleep_cnt = 0
            # 保证程序能够快速退出不用长时间等待
            while sleep_cnt < 100 and self.__thread_run:
                time.sleep(0.1)
                sleep_cnt = sleep_cnt + 1
        self.__sig_finish.emit()
        self.__is_running = False

    def stop(self):
        if self.__thread_run:
            self.__thread_run = False

    def wait(self):
        while self.__is_running:
            time.sleep(0.1)

    def addCodeGeneratedLister(self, func):
        self.__sig_code_generated.connect(func)


class MyAccountBlock(QWidget, AccountBlock):
    sig_worker_start = pyqtSignal()
    sig_worker_stop = pyqtSignal()

    def __init__(self, steam_conf, parent=None):
        super(MyAccountBlock, self).__init__(parent)
        self.setupUi(self)

        self.account.setText(steam_conf.get("steam_username"))
        self.account.show()
        self.__steam_client = MySteamClient(steam_conf, False)
        self.__code_generate_worker = MyCodeGenerateWorker(self.__steam_client)
        self.__workth = QThread()
        self.__code_generate_worker.addCodeGeneratedLister(self.showCode)
        self.__code_generate_worker.moveToThread(self.__workth)
        self.sig_worker_start.connect(self.__code_generate_worker.run)
        self.__workth.start()
        self.sig_worker_start.emit()
        self.showConfirmationButtom.clicked.connect(self.showConfirmations)

        self.account.setAttribute(Qt.WA_TranslucentBackground)
        self.account.setWindowFlags(Qt.FramelessWindowHint)
        self.account.setAlignment(Qt.AlignCenter)
        self.twoFactorCode.setAttribute(Qt.WA_TranslucentBackground)
        self.twoFactorCode.setWindowFlags(Qt.FramelessWindowHint)
        self.twoFactorCode.setAlignment(Qt.AlignCenter)

    def showCode(self, code):
        self.twoFactorCode.setText(code)
        self.twoFactorCode.show()

    def showConfirmations(self):
        # confirmations = self.__steam_client.get_confirmations()
        self.confirmationList = MyConfirmationList()
        self.confirmationList.setWindowModality(Qt.WindowModality.ApplicationModal)
        confirmations = []
        try:
            confirmations = self.__steam_client.get_confirmations()
        except:
            QMessageBox.information(self, "提示", "获取报价失败, 请稍后再试")
            return
        confirmaionBlocks = []
        for confirmation in confirmations:
            myConfirmBlock = MyConfirmBlock(confirmation)
            myConfirmBlock._set_accept(
                lambda trade_offer: self.__steam_client._confirm_transaction(
                    trade_offer
                )
            )
            myConfirmBlock._set_reject(
                lambda trade_offer: self.__steam_client.cancel_trade_offer(trade_offer)
            )
            confirmaionBlocks.append(myConfirmBlock)
        self.confirmationList.showConfirmations(confirmaionBlocks)

    def waitExit(self):
        self.__code_generate_worker.stop()
        self.__code_generate_worker.wait()
