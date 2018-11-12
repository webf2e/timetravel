from util import FileUtil
from util.Global import gloVar

def moveChatFile():
    print("转移聊天记录文件开始")
    FileUtil.renameAndMove(gloVar.chatDirPath)
    print("转移聊天记录文件结束")