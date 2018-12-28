import os,json
from util.Global import gloVar
from service import TravelService

'''
安装步骤：
centos7
yum install wkhtmltopdf
yum install xorg-x11-server-Xvfb

deepin
sudo apt-get install wkhtmltopdf
sudo apt-get install xvfb

中文问题
如果wkhtmltopdf中文显示空白或者乱码方框，下载simsun.ttc字体拷贝到linux服务器/usr/share/fonts/目录下,再次生成pdf中文显示正常

分页问题
table, tr, td, th, tbody, thead, tfoot, div {
    page-break-inside: avoid !important;
}

长表格问题
tr {
    page-break-before: always;
    page-break-after: always;
    page-break-inside: avoid;
}
'''

"""
百度静态图：http://lbsyun.baidu.com/index.php?title=static
"""

def makePdfForTravel():
    gloVar.staticPath="/home/liuwenbin/PycharmProjects/timetravel/static"
    bookDir = os.path.join(gloVar.staticPath, "book")
    #先清理文件
    files = os.listdir(bookDir)
    for file in files:
        filePath = os.path.join(bookDir,file)
        if os.path.isfile(filePath):
            os.remove(filePath)
    #生成html文件
    tempLines = open(os.path.join(bookDir,"temp/temp.html"))
    finalHtml = ""
    for tempLine in tempLines:
        tempLine = tempLine.strip()
        if "" == tempLine:
            continue
        if tempLine.startswith("##readFile#"):
            file = os.path.join(gloVar.staticPath,tempLine.replace("##readFile#",""))
            finalHtml += getCssContent(file)
            continue
        if tempLine.startswith("#travels"):
            travels = json.loads(TravelService.getByDate("2018年12月"))
            for travel in  travels:
                print(travel)
                finalHtml += """
                <div class="panel panel-primary">
                  <div class="panel-heading">
                    <h3 class="panel-title">{}</h3>
                  </div>
                  <div class="panel-body">
                    <table style='width:100%'>
                        <tr>
                            <td>
                                <img src='http://lovexj.pro{}' style='float: left;width:180px;height:156px;margin-right:10px;margin-bottom:5px'/>
                                <img src="http://api.map.baidu.com/staticimage/v2?ak=0LSHte0xuZrXWUrnkEDIIMfwlOnYfiTA&center={},{}&width=270&height=234&zoom=19&dpiType=ph
                                &markers={},{}" 
                                style='float: left;width:180px;height:156px;margin-right:10px;margin-bottom:5px'/>
                                {}
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <hr/>
                            </td>
                        </tr>
                        <tr>
                            <td>
                            
                            </td>
                        </tr>
                    </table>
                  </div> 
                </div>
                """.format(travel["travelName"],travel["indexImg"],travel["lon"],travel["lat"],travel["lon"],travel["lat"],travel["content"])
            continue
        finalHtml += tempLine + "\n"
    tempLines.close()

    bookHtmlPath = os.path.join(bookDir,"book.html")
    pdfPath = os.path.join(bookDir, "book.pdf")
    bookHtml = open(bookHtmlPath, "w+")
    bookHtml.write(finalHtml)
    bookHtml.close()

    os.system("xvfb-run --server-args=\"-screen 0, 1024x768x24\" wkhtmltopdf {} {}".format(bookHtmlPath,pdfPath))

def getCssContent(fileName):
    cssContent = "<style>\n"
    lines = open(fileName,"r+")
    for line in lines:
        line = line.strip()
        if "" == line:
            continue
        cssContent += line + "\n"
    cssContent += "</style>\n"
    lines.close()
    return cssContent