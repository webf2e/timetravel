import os

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

def makePdfForTravel():
    os.system("xvfb-run --server-args=\"-screen 0, 1024x768x24\" wkhtmltopdf http://www.baidu.com aliyun.pdf")