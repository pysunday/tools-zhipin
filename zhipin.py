#coding: utf-8
import os
import sys
import re
import argparse
from pprint import pprint
from sunday.tools.zhipin import config
from sunday.login.zhipin import Zhipin as ZhipinLogin
from sunday.login.zhipin.config import getUserInfo
from sunday.tools.zhipin.params import ZHIPIN_CMDINFO
from sunday.core import Logger, getParser
from pydash import get, find

class Zhipin():
    def __init__(self, isInit=True):
        self.logger = Logger('ZHIPIN HANDLER').getLogger()
        self.userInfo = None
        self.geekFriendList = None
        self.bossInfo = {}
        if isInit: self.init()

    def init(self):
        self.zhipin = ZhipinLogin().login().rs

    def getUserInfo(self):
        if self.userInfo: return self.userInfo
        self.userInfo = self.zhipin.get(getUserInfo).json()['zpData']
        # self.logger.debug('userInfo: %s' % self.userInfo)
        return self.userInfo

    def getToken(self):
        token = self.getUserInfo()['token']
        # self.logger.debug('token: %s' % token)
        return token

    def getPassword(self):
        wt = self.zhipin.get(config.wt).json()
        password = get(wt, 'zpData.wt2')
        # self.logger.debug('password: %s' % password)
        return password

    def getCookies(self):
        cookieObj = self.zhipin.getCookiesDict()
        cookieArr = ['{}={}'.format(key, val) for (key, val) in cookieObj.items()]
        cookieStr = '; '.join(cookieArr)
        # self.logger.debug('cookies: %s' % cookieStr)
        return cookieStr

    def getGeekFriendList(self):
        if not self.geekFriendList:
            res = self.zhipin.get(config.getGeekFriendListUrl).json()
            self.geekFriendList = get(res, 'zpData.result')
            # self.logger.debug('geekFriendList: %s' % self.geekFriendList)
        return self.geekFriendList

    def getGeekFriend(self, uid):
        friends = self.getGeekFriendList()
        friend = find(friends, lambda f: f.get('uid') == int(uid))
        # self.logger.debug('getGeekFriend: %d => %s' % (int(uid), friend))
        return friend

    def bossdata(self, uid, source=0):
        res = self.zhipin.get(config.bossdataUrl % (int(uid), source)).json()
        ans = (get(res, 'zpData.data'), get(res, 'zpData.job'))
        # self.logger.debug('bossdata: %d => %s' % (int(uid), ans))
        return ans

    def historyMsg(self, bossId, count=20, page=1, mid=None):
        # 获取聊天记录
        res = self.zhipin.get(config.historyMsgUrl % (bossId, count, page)).json()
        ans = get(res, 'zpData.messages')
        if mid and type(ans) == list:
            ans = find(ans, lambda m: m.get('mid') == mid)
        # self.logger.debug('historyMsg: %s => %s' % (bossId, ans))
        return ans

    def getHistoryMsg(self, uid, count=20, page=1, mid=None):
        boss = self.getBossInfo(uid)
        if not boss: return {} if mid else []
        ans = self.historyMsg(boss.get('encryptBossId'), count, page, mid=mid)
        return ans

    def getBossInfo(self, uid):
        # 获取boss信息
        if uid in self.bossInfo: return self.bossInfo[uid]
        bossInfo = self.bossdata(uid)[0]
        if bossInfo:
            self.bossInfo[bossInfo.get(uid)] = bossInfo
        return bossInfo


class ZhipinSelf(Zhipin):
    def __init__(self):
        Zhipin.__init__(self, False)

    def bossHandler(self):
        # boss子命令
        if len(self.bossId):
            boss = self.getBossInfo(self.bossId[0])
            pprint(boss)

    def userHandler(self):
        # user子命令
        user = self.getUserInfo()
        pprint(user)

    def friendHandler(self):
        # 历史聊天用户信息
        if self.friendId:
            pprint(self.getGeekFriend(self.friendId))
        else:
            pprint(self.getGeekFriendList())

    def historyHandler(self):
        # history子命令
        if len(self.bossId):
            history = self.getHistoryMsg(self.bossId[0], mid=self.messageId)
            pprint(history)

    def run(self):
        self.init()
        if self.subName == 'boss':
            self.bossHandler()
        elif self.subName == 'user':
            self.userHandler()
        elif self.subName == 'friend':
            self.friendHandler()
        elif self.subName == 'history':
            self.historyHandler()


def runcmd():
    (parser, subparsersObj) = getParser(**ZHIPIN_CMDINFO)
    handle = parser.parse_args(namespace=ZhipinSelf())
    handle.run()


if __name__ == "__main__":
    runcmd()
