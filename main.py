# coding: utf-8
import paho.mqtt.client as mqtt
import time
import random
import json
import certifi
import socks
import os
import logging
from sunday.tools.zhipin.zhipin import Zhipin
from sunday.tools.zhipin.message import chatProtocolDecode
from sunday.tools.zhipin.handler import presenceHandler, textHandler
from sunday.tools.imrobot import Xiaoi
from sunday.core import Logger

messageAutoUid = []

def randomStr(num = 16, rangeNum = 16):
    """生成随机字符串，num为目标字符串长度，rangeNum为字符挑选范围"""
    text = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    ans = [''] * num
    for i in range(num):
        ans[i] = text[random.randint(0, rangeNum - 1)]
    return ''.join(ans)

def readMessageJson():
    messagePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'message.json')
    if not os.path.exists(messagePath): return None
    try:
        with open(messagePath, 'r') as f:
            content = f.read()
            return json.loads(content)
    except Exception as e:
        return None

class ZhipinClient():
    def __init__(self):
        self.logger = Logger('ZHIPIN MQTT').getLogger()
        self.clientId = "ws-" + randomStr()
        self.server = 'ws.zhipin.com'
        self.port = 443
        self.path = '/chatws'
        self.zhipin = Zhipin()
        self.userInfo = self.zhipin.getUserInfo()
        self.password = self.zhipin.getPassword()
        self.cookies = self.zhipin.getCookies()
        self.robot = self.robotInit()
        # 控制未读消息是否回复，保证只统一回复一次, True表示不回复或已经回复过一次
        self.isParsedPresence = True
        self.selfMessageObj = readMessageJson() or {}
        self.isSendTip = []

    def isSelf(self, uid):
        return int(self.userInfo.get('userId')) == int(uid)

    def robotInit(self):
        # 初始化机器人
        robot = Xiaoi()
        robot.open()
        robot.heartbeat()
        return robot

    def on_connect(self, client, userdata, flags, rc):
        self.logger.info("MQTT连接成功, 连接状态: %d" % rc)
        if not self.isParsedPresence:
            self.sendPresence(self.userInfo)
            # time.sleep(1)
            self.autoParseMessage()

    def on_message(self, client, userdata, message):
        self.logger.info('接收到消息, topic: %s, qos: %d, flag: %d' %
                (message.topic, message.qos, message.retain))
        try:
            payload = chatProtocolDecode(message.payload)
            type = payload.get('type')
            msgs = payload.get('messages')
            self.logger.info('消息解码成功')
            self.logger.info('消息类型: %d' % type)
            self.logger.debug(json.dumps(payload, ensure_ascii=False))
            if type == 1:
                self.message_parser_type1(payload)
        except Exception as e:
            self.logger.error('消息解码失败!')
            self.logger.exception(e)

    def message_parser_type1(self, payload):
        # 消息数据解析
        msgs = payload.get('messages')
        msgsLen = len(msgs or [])
        if msgsLen <= 0: return
        self.logger.info('总数据条数: %d' % msgsLen)
        if msgsLen > 1:
            if not self.isParsedPresence:
                self.isParsedPresence = True
            else:
                self.logger.info('未读消息避免重复解析，跳出执行')
                return
        if msgsLen > 0:
            for msg in msgs:
                self.parserMessage(msg)

    def parserMessage(self, msg):
        # 解析并回复消息
        target = msg.get('to')
        origin = msg.get('from')
        body = msg.get('body')
        msgType = msg.get('type')
        bodyType = body.get('type')
        self.logger.debug('parserMessage开始执行 msgType: %d, bodyType: %d' % (msgType, bodyType))
        if self.isSelf(origin.get('uid')):
            self.log.warning('消息为自己发送，跳出')
            return
        type = '%d-%d' % (msgType, bodyType)
        if type in ['1-1', '3-1', '3-8']:
            self.logger.debug('自动回复消息')
            # 为用户发送数据
            bossUid = int(origin.get('uid'))
            text = body.get('text').strip()
            ans = ''
            if type == '3-8' or bossUid not in self.isSendTip:
                # 打招呼或者首次
                ans = self.selfMessageObj['tip']
                self.isSendTip.append(bossUid)
            elif self.selfMessageObj.get(text):
                while self.selfMessageObj.get(text):
                    text = self.selfMessageObj.get(text)
                ans = text
            else:
                ans = self.robot.askText(text)
            self.logger.debug('发送消息: %s' % ans)
            self.sendMessage(ans, target, origin)

    def autoParseMessage(self):
        # 主动发消息
        bossList = self.zhipin.getGeekFriendList()
        for boss in bossList:
            bossUid = int(boss.get('uid'))
            if bossUid in messageAutoUid and bossUid not in self.isSendTip:
                self.isSendTip.append(bossUid)
                self.sendMessage(self.selfMessageObj['intro'], { 'uid': int(self.userInfo.get('userId')) }, { 'uid': bossUid, 'name': boss.get('encryptBossId') })
                self.sendMessage(self.selfMessageObj['tip'], { 'uid': int(self.userInfo.get('userId')) }, { 'uid': bossUid, 'name': boss.get('encryptBossId') })

    def sendMessage(self, text, origin, target):
        # 发送消息
        (boss,) = self.zhipin.bossdata(target.get('uid'))
        if not boss: self.logger.error('uid置换encryptBossId失败')
        (data, buff) = textHandler(text, origin, { **target, 'encryptUid': boss.get('encryptBossId') })
        self.logger.warning('发送请求：%s' % str(data))
        self.send('chat', buff, 1, True)
        # time.sleep(0.5)

    def sendPresence(self, userInfo):
        # 查询未读消息
        cookieA = self.zhipin.zhipin.getCookiesDict().get('__a')
        uniqid = ''
        if cookieA:
            [a, b, *_] = cookieA.split('.')
            uniqid = '.'.join([b, a])
        (data, buff) = presenceHandler(userInfo, uniqid)
        self.logger.warning('发送请求：%s' % str(data))
        self.send('chat', buff, 1, True)

    def send(self, *params):
        self.client.publish(*params)

    def init(self):
        client = mqtt.Client(client_id=self.clientId, transport='websockets')
        client.enable_logger(self.logger)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.username_pw_set(self.userInfo['token'] + '|0', self.password)
        client.ws_set_options(self.path, headers={ 'Cookie': self.cookies })
        client.tls_set(certifi.where())
        client.tls_insecure_set(True)
        # client.proxy_set(proxy_type=socks.HTTP, proxy_addr='127.0.0.1', proxy_port=8888)
        client.connect(self.server, self.port, 60)
        self.client = client

    def run(self):
        try:
            self.client.loop_forever()
            # self.client.loop_start()
        except Exception as e:
            print('Error looping')
            print(e)
        finally:
            self.client.disconnect()

if __name__ == "__main__":
    # readMessageJson()
    zw = ZhipinClient()
    zw.init()
    zw.run()
    # time.sleep(3)
    # zw.parserMessage()
    # zw.sendPresence(zw.userInfo)

