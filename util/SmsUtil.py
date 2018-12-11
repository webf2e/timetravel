import requests, json
from util.Global import gloVar

# 121001	离开你家
# 121000	到你家附近
# 120999	离开家门
# 120997	已经到家
# 120994	离开公司
# 120991	到公司

appkey = "31327b88e60cec38d85ac722d6af2201"
def sendSmsBytempId(mobile, tpl_id):
    sendurl = 'http://v.juhe.cn/sms/send'  # 短信发送的URL,无需修改

    params = 'key=%s&mobile=%s&tpl_id=%s&tpl_value=%s' % \
             (appkey, mobile, tpl_id, "")  # 组合参数

    r = requests.get(sendurl + "?" + params)
    content = r.text  # 获取接口返回内容

    result = json.loads(content)

    if result:
        error_code = result['error_code']
        if error_code == 0:
            # 发送成功
            smsid = result['result']['sid']
            print("sendsms success,smsid: %s" % (smsid))
        else:
            # 发送失败
            print("sendsms error :(%s) %s" % (error_code, result['reason']))
    else:
        # 请求失败
        print("request sendsms error")


def sendFenceModify(jsonMsg):
    if "小可爱的家" in jsonMsg:
        data = jsonMsg["小可爱的家"]
        if 0 == data:
            tempId = 120999
        else:
            tempId = 120997
    elif "小可爱的公司" in jsonMsg:
        data = jsonMsg["小可爱的公司"]
        if 0 == data:
            tempId = 120994
        else:
            tempId = 120991
    elif "亲爱的家" in jsonMsg:
        data = jsonMsg["亲爱的家"]
        if 0 == data:
            tempId = 121001
        else:
            tempId = 121000
    sendSmsBytempId(gloVar.notifyMobile, tempId)