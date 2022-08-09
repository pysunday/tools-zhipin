# coding: utf-8
from sunday.tools.zhipin import zhipin_pb2

def message(type, mid, _from, to, body):
    pb_message= zhipin_pb2.TechwolfMessage()
    pb_message.type = type
    pb_message.mid = mid
    pb_message.cmid = mid
    setattr(pb_message, 'from', _from)
    pb_message.to = to
    pb_message.body = body
    return pb_message
