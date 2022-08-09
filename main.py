# coding: utf-8
import paho.mqtt.client as mqtt
import time
import logging
import random
import json
from sunday.tools.zhipin.zhipin import Zhipin
from sunday.tools.zhipin.message import presence, chatProtocolDecode
import certifi
import socks

def randomStr(num = 16, rangeNum = 16):
    """生成随机字符串，num为目标字符串长度，rangeNum为字符挑选范围"""
    text = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    ans = [''] * num
    for i in range(num):
        ans[i] = text[random.randint(0, rangeNum - 1)]
    return ''.join(ans)

logging.basicConfig(level='DEBUG', format='%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s')



class ZhipinClient():
    def __init__(self):
        self.clientId = "ws-" + randomStr()
        self.server = 'ws.zhipin.com'
        self.port = 443
        self.path = '/chatws'
        self.zhipin = Zhipin()
        self.userInfo = self.zhipin.getUserInfo()
        self.password = self.zhipin.getPassword()
        self.cookies = self.zhipin.getCookies()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.sendPresence(self.userInfo)

    def on_message(self, client, userdata, message):
        print('message topic =', message.topic)
        print('message qos =', message.qos)
        print('message retain flag =', message.retain)
        payload = chatProtocolDecode(message.payload)
        type = payload.get('type')
        msgs = payload.get('messages')
        print('message type =', type, 'message count =', len(msgs))

    def sendPresence(self, userInfo):
        cookieA = self.zhipin.zhipin.getCookiesDict().get('__a')
        uniqid = ''
        if cookieA:
            [a, b, *_] = cookieA.split('.')
            uniqid = '.'.join([b, a])
        params = {
                'type': 1,
                'lastMessageId': 0, # 默认为0，根据数据会有变动
                'clientInfo': {
                    'version': '',
                    'system': '',
                    'systemVersion': '',
                    'model': '',
                    'uniqid': uniqid,
                    'network': userInfo.get('clientIP'),
                    'appid': 9019,
                    'platform': 'web',
                    'channel': '-1',
                    'ssid': '',
                    'bssid': '',
                    'longitude': 0,
                    'latitude': 0
                    }
                }
        payload = presence(params, userInfo.get('userId'))
        self.send('chat', bytearray(payload.SerializeToString()), 1, True)

    def send(self, *params):
        print('发送请求：' + str(params))
        self.client.publish(*params)

    def init(self):
        client = mqtt.Client(client_id=self.clientId, transport='websockets')
        client.enable_logger()
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
    # zw.sendPresence(zw.userInfo)

