# coding: utf-8
import sunday.tools.zhipin.message.model as model
from pydash import get

def sync(data):
    fromUser = model.user(get(data, 'from.uid'), get(data, 'from.encryptUid'), get(data, 'from.source'))
    toUser = model.user(get(data, 'to.uid'), get(data, 'to.encryptUid'), get(data, 'to.source'))
    body = model.body(1, 1)
    body.text = get(data, 'body.text')
    message = model.message(data.get('type') or 1, data.get('tempID'), fromUser, toUser, body)
    chatProtocol = model.chatProtocol(1)
    chatProtocol.message.append(message)
    return chatProtocol

