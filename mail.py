import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import sys
import os
import time
def read_account():
  return ["zhengtianjie@me.com"]
  with open('emailReceiversAccount', 'r+', encoding='utf-8') as f:
      account_li = [account.replace('\n', '') for account in f.readlines()]
      return account_li

def sentemail(send_subject, send_body):
    host = 'smtp.163.com'
    port = 465
    sender = '13007568302@163.com'
    #receivers = ['zhengtianjie@163.com', 'zhenghuijie@1218.com.cn']
    receivers = read_account()
    pwd = '13073shanguangy'
    body = ""
    for node in send_body:
        body = body + "<br><h2>{}</h2><br>".format(node)

    textApart = MIMEText(body, 'html')

    m = MIMEMultipart()
    m.attach(textApart)
    m['Subject'] = send_subject
    m['from'] = sender
    m['to'] = ','.join(receivers)
    
    try:
        server = smtplib.SMTP_SSL(host, port)
        server.login(sender, pwd)
        server.sendmail(sender, receivers, m.as_string())
        print('Done.sent email:%s success' % str(receivers))
        time.sleep(5)
    except smtplib.SMTPException as e:
        print(e)
        print('Error.sent email:%s fail' % str(receivers))

def sentemailPic(send_subject, send_body, pic_path_list):
    host = 'smtp.163.com'
    port = 465
    sender = '13007568302@163.com'
    #receivers = ['zhengtianjie@163.com', 'zhenghuijie@1218.com.cn']
    receivers = read_account()
    pwd = '13073shanguangy'
    body = ""
    for node in send_body:
        body = body + "<br><h2>{}</h2><br>".format(node)

    textApart = MIMEText(body, 'html')

    m = MIMEMultipart()
    m.attach(textApart)

    for pic_path in pic_path_list:
        img1 = MIMEImage(open(pic_path, "rb").read())
        img1.add_header("Content-Disposition", "attachment", filename="1.jpg")
        img1.add_header('Content-ID', 'image1')
        m.attach(img1)
    m['Subject'] = send_subject
    m['from'] = sender
    m['to'] = ','.join(receivers)
    
    try:
        server = smtplib.SMTP_SSL(host, port)
        server.login(sender, pwd)
        server.sendmail(sender, receivers, m.as_string())
        print('Done.sent email:%s success' % str(receivers))
        time.sleep(5)
    except smtplib.SMTPException as e:
        print(e)
        print('Error.sent email:%s fail' % str(receivers))



if __name__ == "__main__":
    sentemail('mail test subject', ['mail test body'])
