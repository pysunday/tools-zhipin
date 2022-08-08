# coding: utf-8
import paho.mqtt.client as mqtt
import time
import logging
import random
from sunday.tools.zhipin.zhipin import Zhipin
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

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # mq_client.subscribe("chat")

    def on_message(self, client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)
        print("message qos=",message.qos)
        print("message retain flag=",message.retain)

    def init(self):
        token = self.zhipin.getToken()
        password = self.zhipin.getPassword()
        cookies = self.zhipin.getCookies()
        client = mqtt.Client(client_id=self.clientId, transport='websockets')
        client.enable_logger()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.username_pw_set(token + '|0', password)
        client.ws_set_options(self.path, headers={ 'Cookie': cookies })
        client.tls_set(certifi.where())
        client.tls_insecure_set(True)
        # client.proxy_set(proxy_type=socks.HTTP, proxy_addr='127.0.0.1', proxy_port=8888)
        client.connect(self.server, self.port, 60)
        self.client = client

    def run(self):
        try:
            self.client.loop_forever()
        except Exception:
            print('Error looping')
        finally:
            self.client.disconnect()

if __name__ == "__main__":
    zw = ZhipinClient()
    zw.init()
    zw.run()

