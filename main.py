# coding: utf-8
import paho.mqtt.client as mqtt
import time
import random
import json
from sunday.tools.zhipin.zhipin import Zhipin
from sunday.tools.zhipin.message import chatProtocolDecode
from sunday.tools.zhipin.handler import presenceHandler, textHandler
from sunday.tools.imrobot import Xiaoi
from sunday.core import Logger
import certifi
import socks

testUid = ''

def randomStr(num = 16, rangeNum = 16):
    """生成随机字符串，num为目标字符串长度，rangeNum为字符挑选范围"""
    text = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    ans = [''] * num
    for i in range(num):
        ans[i] = text[random.randint(0, rangeNum - 1)]
    return ''.join(ans)

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
        self.isParsedPresence = False

    def robotInit(self):
        # 初始化机器人
        robot = Xiaoi()
        robot.open()
        robot.heartbeat()
        return robot

    def on_connect(self, client, userdata, flags, rc):
        self.logger.info("MQTT连接成功, 连接状态: %d" % rc)
        self.sendPresence(self.userInfo)

    def on_message(self, client, userdata, message):
        self.logger.info('接收到消息, topic: %s, qos: %d, flag: %d' %
                (message.topic, message.qos, message.retain))
        try:
            payload = chatProtocolDecode(message.payload)
            type = payload.get('type')
            msgs = payload.get('messages')
            self.logger.info('消息解码成功')
            self.logger.info('信息类型: %d' % type)
            self.logger.debug(json.dumps(payload, indent=2))
            if type == 1 and len(msgs) > 1:
                # 所有未读数据只执行一次解析
                if self.isParsedPresence:
                    msgs = None
                else:
                    self.isParsedPresence = True
            if msgs and len(msgs):
                self.logger.info('数据条数: %d' % len(msgs))
                for msg in msgs:
                    self.parserMessage(msg)

        except Exception as e:
            self.logger.error('信息解码失败!')
            self.logger.error(e)

    def parserMessage(self, msg):
        target = msg.get('to')
        origin = msg.get('from')
        body = msg.get('body')
        msgType = msg.get('type')
        bodyType = body.get('type')
        if msgType == 3 and bodyType == 1:
            # 为用户发送数据
            if int(origin.get('uid')) == int(testUid):
                text = body.get('text')
                ans = self.robot.askText(text)
                self.sendMessage(ans, origin, target)

    def sendMessage(self, text, origin, target):
        # 发送消息
        boss = self.zhipin.getGeekFriend(origin.get('uid'))
        if not boss: self.logger.error('uid置换encryptBossId失败')
        (data, buff) = textHandler(text, target, { **origin, 'encryptUid': boss.get('encryptBossId') })
        self.logger.warning('发送请求：%s' % str(data))
        self.send('chat', buff, 1, True)

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
    zw = ZhipinClient()
    zw.init()
    zw.run()
    time.sleep(3)
    # zw.parserMessage()
    # zw.sendPresence(zw.userInfo)

