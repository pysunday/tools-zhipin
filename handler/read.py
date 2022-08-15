# coding: utf-8
from sunday.tools.zhipin.message import read as msg_read

def readHandler(mid, uid):
    params = { 'uid': int(uid), 'mid': int(mid) }
    payload = msg_read(params)
    return (payload, bytearray(payload.SerializeToString()))

if __name__ == "__main__":
    readHandler(123456, 789120)


