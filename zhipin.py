#coding: utf-8
import os
import sys
import re
import argparse
from sunday.tools.zhipin import config
from sunday.login.zhipin import Zhipin as ZhipinLogin
from sunday.login.zhipin.config import getUserInfo
from sunday.core import Logger, printTable, clear, getParser
from pydash import get, find

class Zhipin():
    def __init__(self):
        self.logger = Logger('ZHIPIN HANDLER').getLogger()
        self.zhipin = ZhipinLogin().login().rs
        self.userInfo = None
        self.geekFriendList = None

    def getUserInfo(self):
        if self.userInfo: return self.userInfo
        self.userInfo = self.zhipin.get(getUserInfo).json()['zpData']
        self.logger.debug('userInfo: %s' % self.userInfo)
        return self.userInfo

    def getToken(self):
        token = self.getUserInfo()['token']
        self.logger.debug('token: %s' % token)
        return token

    def getPassword(self):
        wt = self.zhipin.get(config.wt).json()
        password = get(wt, 'zpData.wt2')
        self.logger.debug('password: %s' % password)
        return password

    def getCookies(self):
        cookieObj = self.zhipin.getCookiesDict()
        cookieArr = ['{}={}'.format(key, val) for (key, val) in cookieObj.items()]
        cookieStr = '; '.join(cookieArr)
        self.logger.debug('cookies: %s' % cookieStr)
        return cookieStr

    def getGeekFriendList(self):
        if not self.geekFriendList:
            res = self.zhipin.get(config.getGeekFriendListUrl).json()
            self.geekFriendList = get(res, 'zpData.result')
            self.logger.debug('geekFriendList: %s' % self.geekFriendList)
        return self.geekFriendList

    def getGeekFriend(self, uid):
        friends = self.getGeekFriendList()
        friend = find(friends, lambda f: f.get('uid') == int(uid))
        self.logger.debug('getGeekFriend: %d => %s' % (int(uid), friend))
        return friend

    def bossdata(self, uid, source=0):
        res = self.zhipin.get(config.bossdataUrl % (int(uid), source)).json()
        ans = (get(res, 'zpData.data'), get(res, 'zpData.job'))
        self.logger.debug('bossdata: %d => %s' % (int(uid), ans))
        return ans

    def run(self):
        self.getCookies()
        self.getUserInfo()
        self.getPassword()


if __name__ == "__main__":
    zhipin = Zhipin()
    # zhipin.getGeekFriend(20525166)
    # zhipin.getUserInfo()
    # zhipin.getGeekFriendList()
    zhipin.bossdata(20525166)
