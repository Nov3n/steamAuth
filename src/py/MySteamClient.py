# coding=utf8
from steampy.client import SteamClient
from steampy.models import TradeOfferState
from steampy.exceptions import InvalidCredentials, CaptchaRequired
from steampy.utils import merge_items_with_descriptions_from_offers
from steampy.guard import load_steam_guard, generate_one_time_code as generate_code
from steampy.confirmation import ConfirmationExecutor
from typing import List
from bs4 import BeautifulSoup
import time
import json


def check_empty(str, hint):
    if len(str) == 0:
        print(hint)
        exit()


class MyConfirmation:
    __steam_client = SteamClient("10D978401D783C20FCE51711B57DEC57")

    def __init__(self, confirmation_details_page):
        self.confirmation_details_page = confirmation_details_page
        self.soup = BeautifulSoup(confirmation_details_page, "html.parser")
        # 仅用于获取steam资料如创建日期

    def get_parter_headline(self) -> str:
        return self.soup.select(".trade_partner_headline_sub")[0].string

    def get_parter_avatar(self) -> str:
        return self.soup.select(".tradeoffer_avatar")[1].img.get("src")

    def get_trade_offer(self) -> str:
        return self.soup.select(".tradeoffer")[0]["id"].split("_")[1]

    def get_parter_steam_id(self) -> str:
        return (
            self.soup.select(".trade_partner_headline_sub")[0]
            .a.get("href")
            .split(".com/profiles/")[1]
        )

    def get_parter_register_date(self) -> str:
        parter_steam_id = (
            self.soup.select(".trade_partner_headline_sub")[0]
            .a.get("href")
            .split(".com/profiles/")[1]
        )
        timecreated = MyConfirmation.__steam_client.get_profile(parter_steam_id).get(
            "timecreated"
        )
        struct_tm = time.gmtime(timecreated)
        return str("{}-{}-{}").format(
            struct_tm.tm_year, struct_tm.tm_mon, struct_tm.tm_mday
        )


class MySteamClient(SteamClient):
    def __init__(self, steam_conf, login_immediate=True):
        self.__steam_conf = steam_conf
        self.__login_immediate = login_immediate
        api_key = steam_conf.get("api_key", "")
        steam_username = steam_conf.get("steam_username", "")
        steam_password = steam_conf.get("steam_password", "")
        check_empty(steam_username, "Empty Username") and check_empty(
            steam_password, "Empty Password"
        ) and check_empty(api_key, "Empty Apikey")
        super(MySteamClient, self).__init__(api_key)
        if len(steam_username) != 0 and login_immediate:
            super(MySteamClient, self).login(
                steam_username, steam_password, json.dumps(steam_conf)
            )

    def get_confirmations(self) -> List[MyConfirmation]:
        if self.__login_immediate:
            confirmations = []
            confirmation_executor = ConfirmationExecutor(
                self.__steam_conf.get("identity_secret"),
                self.__steam_conf.get("steamid"),
                self._session,
            )
            for confirmation in confirmation_executor._get_confirmations():
                confirmation_details_page = (
                    confirmation_executor._fetch_confirmation_details_page(
                        confirmation)
                )
                confirmations.append(MyConfirmation(confirmation_details_page))
            return confirmations
        else:
            steam_username = self.__steam_conf.get("steam_username", "")
            steam_password = self.__steam_conf.get("steam_password", "")
            super(MySteamClient, self).login(steam_username,
                                             steam_password, json.dumps(self.__steam_conf))
            self.__login_immediate = True
            return self.get_confirmations()

    def generate_code(self):
        return generate_code(self.__steam_conf.get("shared_secret"))
