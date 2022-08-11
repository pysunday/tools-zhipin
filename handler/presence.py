# coding: utf-8
from sunday.tools.zhipin.message import presence as msg_presence

def presenceHandler(userInfo, uniqid):
    params = {
            'type': 1,
            'lastMessageId': 0, # 默认为0，根据数据会有变动
            'clientInfo': {
                'version': '',
                'system': '',
                'systemVersion': '',
                'model': '',
                'uniqid': uniqid,
                'network': userInfo.get('clientIP'),
                'appid': 9019,
                'platform': 'web',
                'channel': '-1',
                'ssid': '',
                'bssid': '',
                'longitude': 0,
                'latitude': 0
                }
            }
    payload = msg_presence(params, userInfo.get('userId'))
    return (payload, bytearray(payload.SerializeToString()))

if __name__ == "__main__":
    pass

