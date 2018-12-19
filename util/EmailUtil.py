import smtplib
from email.mime.text import MIMEText
from email.header import Header

def sendEmail(subject,content):
    sender = 'lovexj0818@163.com'
    receivers = ['lovexj0818@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header("爱的小窝", 'utf-8')  # 发送者
    message['To'] = Header("lovexj0818", 'utf-8')  # 接收者

    message['Subject'] = Header(subject, 'utf-8')

    smtp = smtplib.SMTP()
    smtp.connect('smtp.163.com:25')
    smtp.login("lovexj0818", "54liuWENBIN")
    smtp.sendmail(sender, receivers, message.as_string())
    smtp.quit()