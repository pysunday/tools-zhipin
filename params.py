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

ZHIPIN_CHAT_CMDINFO = {
    "version": '0.0.1',
    "description": "zhipin聊天工具",
    "epilog": """
使用案例:
    %(prog)s --robot --config
    %(prog)s --robot --config /path/to/name.json --message-out /path/to/message.log
    %(prog)s --robot --config /path/to/name.json --playback --messsage-in /path/to/message.log
    """,
    'params': {
        'DEFAULT': [
            {
                'name': ['--config'],
                'dest': 'msgConfigFile',
                'metavar': 'FILE',
                'help': '消息映射的json文件',
                'nargs': 1,
                'type': argparse.FileType('r')
            },
            {
                'name': ['--message-in'],
                'dest': 'msgCacheFileIn',
                'metavar': 'FILE',
                'help': '读取消息文件用于回放使用，在--playback下生效，默认为执行目录下的message.cache.log文件',
                'const': './message.cache.log',
                'nargs': '?',
                'type': argparse.FileType('r')
            },
            {
                'name': ['--message-out'],
                'dest': 'msgCacheFileOut',
                'metavar': 'FILE',
                'help': '消息保存文件，用于之后回放使用，默认为执行目录下的message.cache.log文件',
                'const': './message.cache.log',
                'nargs': '?',
                'type': argparse.FileType('w')
            },
            {
                'name': ['--robot'],
                'dest': 'isRobot',
                'help': '是否使用机器人回复消息',
                'default': False,
                'action': 'store_true'
            },
            {
                'name': ['--robot-open'],
                'dest': 'isRobotDefaultOpen',
                'help': '是否默认开启智能回复',
                'default': False,
                'action': 'store_true'
            },
            {
                'name': ['--playback'],
                'dest': 'isPlayback',
                'help': '是否使用本地消息回放',
                'default': False,
                'action': 'store_true'
            },
        ]
    }
}
