# coding: utf-8
import sunday.tools.zhipin.message.model as model

def sync(data):
    messageRead = model.messageSync(data.get('clientMid'), data.get('serverMid'))
    chatProtocol = model.chatProtocol(5)
    chatProtocol.messageSync.append(messageRead)
    return chatProtocol

