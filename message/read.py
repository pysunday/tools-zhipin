# coding: utf-8
import sunday.tools.zhipin.message.model as model

def read(data):
    messageRead = model.messageRead(data.get('uid'), data.get('mid'))
    chatProtocol = model.chatProtocol(6)
    chatProtocol.messageRead.append(messageRead)
    return chatProtocol
