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
            'seconds': 60 * 60 * 2
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
            'func': 'sche.schedule:removeSystemFileJob',
            'args': None,
            'trigger': 'interval',
            'seconds': 10 * 60
        }
    ]

    SCHEDULER_API_ENABLED = True