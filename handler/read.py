# coding: utf-8
from sunday.tools.zhipin.message import read as msg_read

def presenceHandler(userInfo, uniqid):
    params = {
            'uid': '',
            'mid': '',
            'source': 0
            }
    payload = msg_read(params)
    return (payload, bytearray(payload.SerializeToString()))

if __name__ == "__main__":
    pass


