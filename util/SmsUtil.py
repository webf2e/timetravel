import requests, json, logging
from util.Global import gloVar
from util import CommonUtil

# 121001	离开你家
# 121000	到你家附近
# 120999	离开家门
# 120997	已经到家
# 120994	离开公司
# 120991	到公司
# 121042    末次位置数据无更新提示

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
            logging.warning("sendsms success,smsid: %s" % (smsid))
        else:
            # 发送失败
            logging.warning("sendsms error :(%s) %s" % (error_code, result['reason']))
    else:
        # 请求失败
        logging.warning("request sendsms error")


def sendFenceModify(jsonMsg):
    sendSmsBytempId(gloVar.notifyMobile, CommonUtil.getTempIdAndContent(jsonMsg)["tempId"])