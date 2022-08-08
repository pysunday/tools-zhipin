# coding: utf-8
from sunday.tools.zhipin import zhipin_pb2

def chatProtocol(type):
    pb_chatProtocol = zhipin_pb2.TechwolfChatProtocol()
    pb_chatProtocol.type = type
    return pb_chatProtocol

