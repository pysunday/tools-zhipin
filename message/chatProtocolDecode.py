# coding: utf-8
from sunday.tools.zhipin import zhipin_pb2
from google.protobuf import json_format

def chatProtocolDecode(message):
    pb_chatProtocol = zhipin_pb2.TechwolfChatProtocol()
    pb_chatProtocol.ParseFromString(message)
    return json_format.MessageToDict(pb_chatProtocol)
    

