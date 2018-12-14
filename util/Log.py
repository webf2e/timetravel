import logging
import logging.handlers
from util.Global import gloVar

def init():
    logging.basicConfig()
    root = logging.getLogger()
    root.setLevel(logging.WARNING)
    filehandler = logging.FileHandler(filename=gloVar.loggingFilePath)
    format = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    filehandler.setFormatter(format)
    filehandler.suffix = "%Y-%m-%d.log"
    root.addHandler(filehandler)