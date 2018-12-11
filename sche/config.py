class Config(object):
    JOBS = [
        {
            'id': 'moveChatFileJob',
            'func': 'sche.schedule:moveChatFileJob',
            'args': None,
            'trigger': 'interval',
            'seconds': 10
        },
        {
            'id': 'makeBigHeartJob',
            'func': 'sche.schedule:makeBigHeartJob',
            'args': None,
            'trigger': 'interval',
            'seconds': 60 * 60 * 6
        },
        {
            'id': 'systemTongjiJob',
            'func': 'sche.schedule:systemTongjiJob',
            'args': None,
            'trigger': 'interval',
            'seconds': 5
        },
        {
            'id': 'removeSystemFileJob',
            'func': 'sche.schedule:removeFileJob',
            'args': None,
            'trigger': 'interval',
            'seconds': 20 * 60
        },
        {
            'id': 'getChatMessageFromChatImg',
            'func': 'sche.schedule:getChatMessageFromChatImg',
            'args': None,
            'trigger': 'interval',
            'seconds': 60 * 60
        },
        {
            'id': 'checkLastLocationJob',
            'func': 'sche.schedule:checkLastLocationJob',
            'args': None,
            'trigger': 'interval',
            'seconds': 30
        }
    ]

    SCHEDULER_API_ENABLED = True