
# 121001	离开你家
# 121000	到你家附近
# 120999	离开家门
# 120997	已经到家
# 120994	离开公司
# 120991	到公司
# 121042    末次位置数据无更新提示

def getTempIdAndContent(jsonMsg):
    result = {}
    if "小可爱的家" in jsonMsg:
        data = jsonMsg["小可爱的家"]
        if 0 == data:
            result["tempId"] = 120999
            result["content"] = "已离开家"
        else:
            result["tempId"] = 120997
            result["content"] = "已到家"
    elif "小可爱的公司" in jsonMsg:
        data = jsonMsg["小可爱的公司"]
        if 0 == data:
            result["tempId"] = 120994
            result["content"] = "已离开公司"
        else:
            result["tempId"] = 120991
            result["content"] = "已到公司"
    elif "亲爱的家" in jsonMsg:
        data = jsonMsg["亲爱的家"]
        if 0 == data:
            result["tempId"] = 121001
            result["content"] = "已离开亲爱的家"
        else:
            result["tempId"] = 121000
            result["content"] = "已到亲爱的家"
    return result