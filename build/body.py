# coding: utf-8
from sunday.tools.zhipin import zhipin_pb2

def body(type, templateId):
    pb_body = zhipin_pb2.TechwolfMessageBody()
    pb_body.type = type
    pb_body.templateId = templateId
    return pb_body
