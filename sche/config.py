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
        },
        {
            'id': 'locationTongjiJob',
            'func': 'sche.schedule:locationTongjiJob',
            'args': None,
            'trigger': 'interval',
            'seconds': 10 * 60
        },
        {
            'id': 'setFenceNotifySlienceJob',
            'func': 'sche.schedule:setFenceNotifySlienceJob',
            'args': None,
            'trigger': {
                'type': 'cron',
                'day_of_week':"mon-sun",
                'hour':'23',
                'minute':'0',
                'second': '0'
            }
        },
        {
            'id': 'splitLogJob',
            'func': 'sche.schedule:splitLogJob',
            'args': None,
            'trigger': {
                'type': 'cron',
                'day_of_week':"mon-sun",
                'hour':'0',
                'minute':'0',
                'second': '0'
            }
        },
        {
            'id': 'delOtherLogJob',
            'func': 'sche.schedule:delOtherLogJob',
            'args': None,
            'trigger': {
                'type': 'cron',
                'day_of_week':"mon-sun",
                'hour':'0',
                'minute':'10',
                'second': '0'
            }
        }
    ]

    SCHEDULER_API_ENABLED = True