# coding: utf-8
from sunday.tools.zhipin import zhipin_pb2
from sunday.tools.zhipin.build.clientInfo import clientInfo

def presence(info, uid):
    pb_presence = zhipin_pb2.TechwolfPresence()
    pb_presence.clientInfo = clientInfo(info.get('clientInfo') or {})
    pb_presence.uid = uid
    pb_presence.type = info['type']
    pb_presence.lastMessageId = info['lastMessageId']
    return pb_presence

