class redisKey():
    #setting类型

    #是否进行围栏通知的开关
    isNeedFenceInOutNotify = "isNeedFenceInOutNotify"
    #当位置长时间不更新时，是否进行短信通知
    isNeedLocationNotUpdateForSmsNotify = "isNeedLocationNotUpdateForSmsNotify"
    #当位置长时间不更新时，是否进行app推送通知
    isNeedLocationNotUpdateForAppNotify = "isNeedLocationNotUpdateForAppNotify"
    # app的客户端ID（个推）
    cid = "cid"


    #有ttl的

    # 是否发送过没有位置更新时的app推送
    locationNotUpdatePush = "locationNotUpdatePush"
    # 是否发送过没有位置更新时的短信通知
    locationNotUpdateSms = "locationNotUpdateSms"
    # 是否发生过围栏报警
    lastFenceTime = "lastFenceTime"
    # 是否在围栏通知的围绕模式中
    fenceNotifySlience = "fenceNotifySlience"
    # 是否已经发生了磁盘报警
    diskAlarm = "diskAlarm"
    # 从baidu鹰眼获取的末次位置缓存
    lastLocationFromBaidu = "lastLocationFromBaidu"

    #key类型
    #末次位置
    lastLocation = "lastLocation"
    #上次围栏的状态
    lastFenceState = "lastFenceState"
    #位置统计
    locationTongji = "locationTongji"