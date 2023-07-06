from ..ui.Ui_AccountBlock import Ui_AccountBlock as AccountBlock
from ..ui.Ui_ConfirmationBlock import Ui_ConfirmationBlock as ConfirmBlock
from ..py.MySteamClient import MySteamClient, MyConfirmation
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests, time


class MyConfirmationsWindow(QWidget):
    pass


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
                    self.show_res(True)
                else:
                    self.show_res(False)
            except:
                self.show_res(False)
        pass

    def reject(self):
        if self.__reject:
            try:
                rsp = self.__reject(self.confirmation.get_trade_offer())
                if rsp.get("success", False):
                    self.show_res(True)
                else:
                    self.show_res(False)
            except:
                self.show_res(False)
        pass

    def show_res(self, res):
        self.confirm.deleteLater()
        self.cancel.deleteLater()
        label = QLabel()
        res_str = str("确认失败")
        if res:
            res_str = str("确认成功")
        label.setText(res_str)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.confirmRes.setLayout(layout)

    def _set_accept(self, accept_func):
        self.__accept = accept_func

    def _set_reject(self, reject_func):
        self.__reject = reject_func


class MyCodeGenerateWorker(QObject):
    sig_code_generated = pyqtSignal(str)
    sig_finish = pyqtSignal()
    thread_run = True

    def __init__(self, steam_client):
        super(MyCodeGenerateWorker, self).__init__()
        self.thread_run = True
        self._steam_client = steam_client

    def run(self):
        while self.thread_run:
            self.sig_code_generated.emit(self._steam_client.generate_code())
            time.sleep(15)
        self.sig_finish.emit()


class MyAccountBlock(QWidget, AccountBlock):
    sig_worker_start = pyqtSignal()
    sig_worker_stop = pyqtSignal()

    def __init__(self, steam_conf, parent=None):
        super(MyAccountBlock, self).__init__(parent)
        self.setupUi(self)

        self.account.setText(steam_conf.get("steam_username"))
        self.account.show()
        self.__steam_client = MySteamClient(steam_conf)
        self.__code_generate_worker = MyCodeGenerateWorker(self.__steam_client)
        self.__workth = QThread()
        self.__code_generate_worker.sig_code_generated.connect(self.showCode)
        self.__code_generate_worker.moveToThread(self.__workth)
        self.sig_worker_start.connect(self.__code_generate_worker.run)
        self.__workth.start()
        self.sig_worker_start.emit()
        self.showConfirmationButtom.clicked.connect(self.showConfirmations)

        self.account.setAttribute(Qt.WA_TranslucentBackground)
        self.account.setWindowFlags(Qt.FramelessWindowHint)
        self.twoFactorCode.setAttribute(Qt.WA_TranslucentBackground)
        self.twoFactorCode.setWindowFlags(Qt.FramelessWindowHint)

    def showCode(self, code):
        self.twoFactorCode.setText(code)
        self.twoFactorCode.show()

    def showConfirmations(self):
        # confirmations = self.__steam_client.get_confirmations()
        self.confirmationsWindow = MyConfirmationsWindow()
        self.confirmationsWindow.resize(400, 500)
        self.confirmationsWindow.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.confirmationsWindow.show()

        confirmations = self.__steam_client.get_confirmations()
        for confirmation in confirmations:
            myConfirmaBlock = MyConfirmBlock(confirmation)

            if not self.confirmationsWindow.layout():
                layout = QVBoxLayout()
                self.confirmationsWindow.setLayout(layout)
            myConfirmaBlock.show()
            self.confirmationsWindow.layout().addWidget(myConfirmaBlock)
            myConfirmaBlock._set_accept(
                lambda trade_offer: self.__steam_client._confirm_transaction(
                    trade_offer
                )
            )
            myConfirmaBlock._set_reject(
                lambda trade_offer: self.__steam_client.cancel_trade_offer(trade_offer)
            )
