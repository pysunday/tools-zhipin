# coding: utf-8
import paho.mqtt.client as mqtt
import time
import random
import json
import certifi
import socks
import os
from sunday.tools.zhipin.zhipin import Zhipin
from sunday.tools.zhipin.message import chatProtocolDecode
from sunday.tools.zhipin.handler import presenceHandler, textHandler, iqHandler, readHandler
from sunday.tools.zhipin.params import ZHIPIN_CHAT_CMDINFO
from sunday.tools.imrobot import Xiaoi
from sunday.core import Logger, getParser
from pydash import get

messageAutoUid = []

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
        # 聊天机器人
        self.robot = None
        # zhipin登录交互
        self.zhipin = None
        # 当前登录用户
        self.userInfo = None
        # 当前mutt密码
        self.password = None
        # 当前登录的cookie
        self.cookies = None
        # 控制未读消息是否回复，保证只统一回复一次, True表示不回复或已经回复过一次
        self.isParsedPresence = True
        # 回复模版对象
        self.selfMessageObj = {}
        # 首次需要发送tip信息，标记已经发送后不再发送
        self.isSendTip = []
        # 即时通讯客户端
        self.client = None
        # 当前正在聊天的boss
        self.currentChatBossId = None
        # 记录开启智能聊天的boss对象
        self.openChatBossStore = {}

    def isSelf(self, uid):
        return int(self.userInfo.get('userId')) == int(uid)

    def on_connect(self, client, userdata, flags, rc):
        self.logger.info("MQTT连接成功, 连接状态: %d" % rc)
        if not self.isParsedPresence:
            self.sendPresence(self.userInfo)
            # time.sleep(1)
            self.autoParseMessage()
        (data, buff) = textHandler('haha', {'uid': 555547565}, {'uid': 27904943, 'encryptUid': 'bfb5c693853bd21d1XNz29m0FFE~' }, self.userInfo)
        self.send('chat', buff, 1, True)

    def on_message(self, client, userdata, message):
        self.logger.info('接收到消息, topic: %s, qos: %d, flag: %d' %
                (message.topic, message.qos, message.retain))
        try:
            payload = chatProtocolDecode(message.payload)
            self.message_parser(payload)
        except Exception as e:
            self.logger.error('消息解码失败!')
            self.logger.exception(e)

    def writeMqttMessage(self, msg):
        # 写入消息
        if self.msgCacheFileOut:
            self.msgCacheFileOut.write(msg + '\n')

    def message_parser(self, payload):
        # 解析payload
        type = payload.get('type')
        msgs = payload.get('messages')
        self.logger.info('消息解码成功')
        self.logger.info('消息类型: %d' % type)
        msg = json.dumps(payload, ensure_ascii=False)
        self.writeMqttMessage(msg)
        self.logger.debug(msg)
        if type in [1, 3]:
            self.message_parser_type1(payload)
        elif type in [6]:
            self.message_parser_type6(payload)
        elif type in [4]:
            self.message_parser_type4(payload)

    def message_parser_type4(self, payload):
        # 消息已回复
        resList = get(payload, 'iqResponse.results') or []
        resObj = {}
        for res in resList:
            resObj[res.get('key')] = res.get('value')
        uid = resObj.get('friendId')
        mid = resObj.get('msg_id')
        if self.isSelf(uid) or not uid or not mid: return
        message = self.zhipin.getHistoryMsg(uid, mid=mid)
        if message:
            self.logger.info('消息已回复(%s): %s' % (get(message, 'to.name'), message.get('pushText')))

    def message_parser_type6(self, payload):
        # 消息已读
        uid = get(payload, 'messageRead.0.userId')
        mid = get(payload, 'messageRead.0.messageId')
        if uid: uid = int(uid)
        if mid: mid = int(mid)
        if self.isSelf(uid):
            self.logger.info('自己查看了信息')
        elif mid:
            message = self.zhipin.getHistoryMsg(uid, mid=mid)
            if message:
                self.logger.info('消息已查看(%s): %s' % (get(message, 'to.name'), message.get('pushText')))
        else:
            bossInfo = self.zhipin.getBossInfo(uid)
            self.logger.info('%s(%s)查看了信息' %s (bossInfo.get(name), bossInfo.get(companyName)))

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
        self.logger.warning('parserMessage开始执行 msgType: %d, bodyType: %d' % (msgType, bodyType))
        if self.isSelf(origin.get('uid')):
            self.logger.warning('消息为自己发送，跳出')
            return
        type = '%d-%d' % (msgType, bodyType)
        ans = ''
        bossId = origin.get('uid')
        bossName = origin.get('name')
        canChat = self.openChatBossStore.get(bossId)
        if type in ['1-1', '3-1']:
            # 为用户发送数据
            text = body.get('text').strip()
            if self.selfMessageObj.get(text) or text in ['openChat']:
                while self.selfMessageObj.get(text) is not None:
                    text = self.selfMessageObj.get(text)
                ans = text
            elif canChat and self.robot:
                ans = self.robot.askText(text)
                if ans in ['', 'defaultReply']:
                    ans = '机器人没有看懂你在说什么'
        elif type == '3-8':
            # 系统打招呼
            bossUid = int(origin.get('uid'))
            if bossUid not in self.isSendTip:
                ans = self.selfMessageObj['tip']
                self.isSendTip.append(bossUid)
        elif type == '1-7' and canChat:
            ans = '这得主人自己决策，稍等哈'
        elif type == '1-20' and canChat:
            ans = '机器人暂时只看得懂文字哦'
        if ans == 'openChat':
            # 开启智能聊天
            self.openChatBossStore[bossId] = not self.openChatBossStore.get(bossId)
            isOpen = self.openChatBossStore[bossId]
            self.logger.warning('%s: %s智能聊天' % (bossName, '开启' if isOpen else '关闭'))
            ans = '已开启智能聊天，智能聊天服务由小i机器人提供' if isOpen else '已关闭智能聊天'
        if ans:
            self.sendMessageRead(msg)
            self.sendMessageIq(msg)
            self.logger.debug('自动回复消息: %s' % ans)
            self.sendMessage(ans, target, origin)

    def sendMessageRead(self, msg):
        # 消息已读
        (data, buff) = readHandler(msg.get('mid'), get(msg, 'from.uid'))
        self.logger.warning('发送消息::sendMessageRead\n%s' % str(data))
        self.send('chat', buff, 1, True)

    def sendMessageIq(self, msg):
        # 开启新会话
        currentChatBossId = int(get(msg, 'from.uid') or 0)
        if currentChatBossId and self.currentChatBossId != currentChatBossId:
            self.currentChatBossId = currentChatBossId
            (data, buff) = iqHandler(msg, self.userInfo.get('userId'))
            self.logger.warning('发送消息::sendMessageIq\n%s' % str(data))
            self.send('chat', buff, 1, True)

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
        (boss, *_) = self.zhipin.bossdata(target.get('uid'))
        if not boss:
            self.logger.error('uid置换encryptBossId失败')
            return
        (data, buff) = textHandler(text, origin, { **target, 'encryptUid': boss.get('encryptBossId') }, self.userInfo)
        self.logger.warning('发送消息::sendMessage\n%s' % str(data))
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
        self.logger.warning('发送消息::sendPresence\n%s' % str(data))
        self.send('chat', buff, 1, True)

    def send(self, *params):
        if self.client: self.client.publish(*params)

    def init(self):
        self.zhipinInit()
        # 初始化智能聊天机器人
        if self.isRobot: self.robotInit()
        # 初始化聊天服务
        if not self.isPlayback: self.muttInit()
        __import__('ipdb').set_trace()
        if self.msgConfigFile:
            # 解析回复模版
            try:
                selfMessageStr = self.msgConfigFile.read()
                self.selfMessageObj = json.loads(selfMessageStr)
            except Exception as e:
                self.logger.error('消息回复模版解析失败，请检查文件%s内容是否为JSON格式'
                        % self.msgConfigFile.name)

    def zhipinInit(self):
        self.zhipin = Zhipin()
        self.userInfo = self.zhipin.getUserInfo()
        self.password = self.zhipin.getPassword()
        self.cookies = self.zhipin.getCookies()

    def robotInit(self):
        # 初始化机器人
        robot = Xiaoi()
        robot.open()
        robot.heartbeat()
        self.robot = robot

    def muttInit(self):
        # 初始化聊天服务
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

    def runByCache(self):
        if not self.msgCacheFileIn:
            self.logger.error('回放模式需要显式调用参数--message-in')
            return
        for msg in self.msgCacheFileIn.readlines():
            if not msg: continue
            payload = json.loads(msg)
            self.message_parser(payload)

    def run(self):
        self.init()
        try:
            if self.client:
                self.client.loop_forever()
            else:
                self.runByCache()
        except Exception as e:
            print('Error looping')
            print(e)
        finally:
            self.client and self.client.disconnect()
            self.msgCacheFileIn and self.msgCacheFileIn.close()
            self.msgCacheFileOut and self.msgCacheFileOut.close()
            self.logger.warning('如果程序未退出可能是robot还在心跳，可按键Ctrl + c终止程序执行')


def runcmd():
    parser = getParser(**ZHIPIN_CHAT_CMDINFO)
    handle = parser.parse_args(namespace=ZhipinClient())
    handle.run()

if __name__ == "__main__":
    runcmd()

