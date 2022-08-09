# coding: utf-8
from sunday.tools.zhipin import zhipin_pb2
from sunday.tools.zhipin.message.model.clientInfo import clientInfo

def presence(info, uid):
    pb_presence = zhipin_pb2.TechwolfPresence()
    pb_presence.clientInfo.CopyFrom(clientInfo(info.get('clientInfo')))
    pb_presence.uid = uid
    pb_presence.type = info.get('type')
    pb_presence.lastMessageId = info.get('lastMessageId')
    return pb_presence

