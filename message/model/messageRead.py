# coding: utf-8
import time
from sunday.tools.zhipin import zhipin_pb2

def messageRead(userId, messageId):
    pb_messageRead = zhipin_pb2.TechwolfMessageRead()
    pb_messageRead.userId = userId
    pb_messageRead.messageId = messageId
    pb_messageRead.readTime = int(time.time() * 1000)
    pb_messageRead.userSource = 0
    return pb_messageRead


