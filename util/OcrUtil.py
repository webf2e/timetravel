from aip import AipOcr

def getContent(imgPath):
    APP_ID = '14966224'
    API_KEY = 'rPhViWQUjGNHsBlIlDResFsw'
    SECRET_KEY = 'eAumx7GpORCoDUmc5NGwHWHds76zgAtl'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    """ 读取图片 """

    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    image = get_file_content(imgPath)

    """ 调用通用文字识别, 图片参数为本地图片 """
    result = client.accurate(image)
    if str(result).find("error_msg") != -1:
        print(result)
        return ""
    return result