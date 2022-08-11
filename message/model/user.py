# coding: utf-8
from sunday.tools.zhipin import zhipin_pb2

def user(uid, name, source):
    pb_user = zhipin_pb2.TechwolfUser()
    pb_user.source = source or 0
    pb_user.uid = uid or 0
    if uid and name:
        pb_user.name = name
    return pb_user
