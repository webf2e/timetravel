class Config(object):
    JOBS = [
        {
            'id': 'moveChatFileJob',
            'func': 'sche.schedule:moveChatFile',
            'args': None,
            'trigger': 'interval',
            'seconds': 10
        }
    ]

    SCHEDULER_API_ENABLED = True