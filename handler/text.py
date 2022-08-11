# coding: utf-8
import time
from pydash import pick
from sunday.tools.zhipin.message import text as msg_text

def textHandler(text, source, target):
    sourceCopy = pick(source, ['uid', 'encryptUid', 'source'])
    targetCopy = pick(target, ['uid', 'encryptUid', 'source'])
    __import__('ipdb').set_trace()
    message = {
        "tempID": 1660167577200,
        "isSelf": True,
        "body": {
            "type": 1,
            "text": text,
            "sticker": None
        },
        "from": sourceCopy,
        "to": targetCopy,
        # "encryptUid": "9efdaee8ae5c9bdd1nZ62NS9EFdS"
        "time": int(time.time() * 1000),
        "mSource": "server",
        "typeSource": "newSubmit",
        "type": 1,
        "isSelf": True
    }
    payload = msg_text(message)
    return (payload, bytearray(payload.SerializeToString()))

if __name__ == "__main__":
    kk = {"tempID":1660167577200,"isSelf":True,"body":{"type":1,"text":"测试","sticker":None},"from":{"uid":27904943,"name":"陈滔"},"to":{"uid":120390052,"source":"","encryptUid":"9efdaee8ae5c9bdd1nZ62NS9EFdS"},"time":1660139672257,"mSource":"server","typeSource":"newSubmit","type":1}
    textHandler('haha', kk['from'], kk['to'])

