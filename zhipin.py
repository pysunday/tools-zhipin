# coding: utf-8
import os
import sys
import re
import argparse
from sunday.tools.zhipin import config
from sunday.login.zhipin import Zhipin as ZhipinLogin
from sunday.login.zhipin.config import getUserInfo
from sunday.core import Logger, printTable, clear, getParser
from pydash import get

class Zhipin():
    def __init__(self):
        self.zhipin = ZhipinLogin().login().rs

    def getToken(self):
        info = self.zhipin.get(getUserInfo).json()
        token = get(info, 'zpData.token')
        print('token: %s' % token)
        return token

    def getPassword(self):
        wt = self.zhipin.get(config.wt).json()
        password = get(wt, 'zpData.wt2')
        print('password: %s' % password)
        return password

    def getCookies(self):
        cookieObj = self.zhipin.getCookiesDict()
        cookieArr = ['{}={}'.format(key, val) for (key, val) in cookieObj.items()]
        cookieStr = '; '.join(cookieArr)
        print(cookieStr)
        return cookieStr

    def run(self):
        self.getCookies()
        self.getToken()
        self.getPassword()


if __name__ == "__main__":
    Zhipin().run()
