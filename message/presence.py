# coding: utf-8
import sunday.tools.zhipin.message.model as model

def presence(data, uid):
    presence = model.presence(data, uid)
    chatProtocol = model.chatProtocol(2)
    chatProtocol.presence.CopyFrom(presence)
    return chatProtocol
