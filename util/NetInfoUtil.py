import requests
from bs4 import BeautifulSoup

def getMovieType(movieName):
    url = "https://maoyan.com/query?kw={}".format(movieName)
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    divs = soup.find_all(class_="movie-item-cat")
    if len(divs) > 0:
        type = divs[0].text.strip()
        if "" != type:
            return type
    return "暂无类型"