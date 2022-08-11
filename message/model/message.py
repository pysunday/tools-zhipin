# coding: utf-8
from sunday.tools.zhipin import zhipin_pb2

def message(type, mid, _from, to, body):
    pb_message= zhipin_pb2.TechwolfMessage()
    pb_message.type = type
    pb_message.mid = mid
    pb_message.cmid = mid
    getattr(pb_message, 'from').CopyFrom(_from)
    pb_message.to.CopyFrom(to)
    pb_message.body.CopyFrom(body)
    return pb_message
