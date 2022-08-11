# coding: utf-8
import sunday.tools.zhipin.message.model as model
from pydash import get

def text(data):
    fromUid = int(get(data, 'from.uid'))
    toUid = int(get(data, 'to.uid'))
    fromUser = model.user(fromUid, get(data, 'from.encryptUid'), get(data, 'from.source'))
    toUser = model.user(toUid, get(data, 'to.encryptUid'), get(data, 'to.source'))
    body = model.body(1, 1)
    body.text = get(data, 'body.text')
    message = model.message(data.get('type') or 1, data.get('tempID'), fromUser, toUser, body)
    message.time = data.get('time')
    message.isSelf = data.get('isSelf')
    chatProtocol = model.chatProtocol(1)
    chatProtocol.messages.append(message)
    return chatProtocol

