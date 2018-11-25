class Config(object):
    JOBS = [
        {
            'id': 'moveChatFileJob',
            'func': 'sche.schedule:moveChatFile',
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
        }
    ]

    SCHEDULER_API_ENABLED = True