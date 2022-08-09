# coding: utf-8
from sunday.tools.zhipin import zhipin_pb2

def messageSync(clientMid, serverMid):
    pb_messageSync = zhipin_pb2.TechwolfMessage()
    pb_messageSync.clientMid = clientMid
    pb_messageSync.serverMid = serverMid
    return pb_messageSync

