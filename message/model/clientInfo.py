from sunday.tools.zhipin import zhipin_pb2

def clientInfo(info):
    keys = ['version', 'system', 'systemVersion', 'model', 'uniqid', 'network', 'appid', 'platform', 'channel', 'ssid', 'bssid', 'longitude', 'latitude']
    pb_clientInfo = zhipin_pb2.TechwolfClientInfo()
    for key in keys:
        if info.get(key) is not None:
            setattr(pb_clientInfo, key, info[key])
    return pb_clientInfo

