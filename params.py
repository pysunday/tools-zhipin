# coding: utf-8
import argparse

ZHIPIN_CMDINFO = {
    "version": '0.0.1',
    "description": "zhipin查询工具",
    "epilog": """
使用案例:
    %(prog)s boss 20521234
    %(prog)s user
    %(prog)s friend 20521234
    %(prog)s history 112051234
    %(prog)s history 112051234 -m 321012345678
    """,
    'params': {
        'SUBCONFIG': {
            'title': '子命令',
            'dest': 'subName'
        },
        'boss': [
            {
                'name': ['bossId'],
                'help': 'boss唯一标识，即bossUid',
                'nargs': 1,
                'type': int
            },
        ],
        'history': [
            {
                'name': ['bossId'],
                'help': 'boss唯一标识，即bossUid',
                'nargs': 1,
                'type': int
            },
            {
                'name': ['-m', '--mid'],
                'dest': 'messageId',
                'help': '消息ID',
                'type': int
            },
        ],
        'user': [ ],
        'friend': [
            {
                'name': ['friendId'],
                'help': '聊过天朋友的唯一ID',
                'nargs': '?',
                'type': int
            }
        ]
    }
}

