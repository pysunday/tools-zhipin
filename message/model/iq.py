# coding: utf-8
from sunday.tools.zhipin import zhipin_pb2

def iq(data):
    pb_iq = zhipin_pb2.TechwolfIq()
    pb_kvEntry = zhipin_pb2.TechwolfKVEntry()
    params = data.get('params') or {}
    for [key, val] in params.items():
        pb_kvEntry.key = key
        pb_kvEntry.value = str(val)
        pb_iq.params.append(pb_kvEntry)
    pb_iq.query = data.get('query')
    pb_iq.qid = data.get('qid')
    return pb_iq
