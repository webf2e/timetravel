import logging
from util.Global import gloVar

def get():
    logging.basicConfig(level=logging.INFO,
                        filename="/home/liuwenbin/Desktop/program/pythonLog/1.log",
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    return logging.getLogger("logg")