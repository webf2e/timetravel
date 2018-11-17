from util import FileUtil
from util.Global import gloVar
from service import TravelService

def moveChatFile():
    print("转移聊天记录文件开始")
    FileUtil.renameAndMove(gloVar.chatDirPath)
    print("转移聊天记录文件结束")

def reloadGallery():
    print("重新加载gallery开始")
    gloVar.monthImgMap = FileUtil.getGalleryImgByMonth(TravelService.getIdTimeLast3Month())
    print(gloVar.monthImgMap)
    print("重新加载gallery结束")