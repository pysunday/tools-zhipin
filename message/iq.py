# coding: utf-8
import sunday.tools.zhipin.message.model as model

def iq(data):
    iq = model.iq(data)
    chatProtocol = model.chatProtocol(3)
    chatProtocol.iq.CopyFrom(iq)
    return chatProtocol
