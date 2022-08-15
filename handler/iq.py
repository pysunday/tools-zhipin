# coding: utf-8
from sunday.tools.zhipin.message import iq as msg_iq
from pydash import get
from time import time

def iqHandler(data, selfId: int):
    target = data.get('to' if int(get(data, 'from.uid')) == selfId else 'from')
    params = {
            'qid': int(time() * 1000),
            'params': {
                'action': 'query',
                'from_id': selfId,
                'to_id': target.get('uid'),
                'friend_source': get(data, 'from.source'),
                'msg_id': data.get('mid')
                },
            'query': '/message/suggest'
            }
    payload = msg_iq(params)
    return (payload, bytearray(payload.SerializeToString()))

if __name__ == "__main__":
    pass

