'''
==============================================
**email_auto**: sending emails automatically.
==============================================
:author: Chufeng LI
:email:  chufeng.li@cfel.de
:date:   2020-05-07
'''
import sys,os
import smtplib
import imghdr
import datetime
from email.message import EmailMessage
import time
import datetime
import glob
import imghdr

def mail_auto_beta(Contact_list,sending_time):
    User_name = 'lichufen'
    Pass_word = os.environ.get('Email_password')
    Host_name = 'smtp-auth.desy.de'


    body = '''\
Dear Friends：
亲爱的朋友：
Hello, from Email Automation Assistant!
您好， 来自 自动邮件助手的问候！:)
This is a plain-text message, which has been sent for testing the timing accuracy of the system.
这是一条纯文本消息, 此次发送是为了测试系统的时间准确性。

The sending time is May 8th 01:40:00（CET）. In case you got this message, could you kindly reply with the time stamp it was received(for a favor)?
发送时间为 5月8日 01：40：00（欧洲中部时间）。如果您成功收到这封邮件，请您帮忙回复一下，附上收件时标。
Thanks!
多谢多谢！
Yours,
Chufeng Li

祝好，
李楚峰
            '''
    while datetime.datetime.now() < sending_time:
        delta = sending_time - datetime.datetime.now()
        print('time left: %s'%(str(delta)))
        time.sleep(1)
    with smtplib.SMTP(Host_name,587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(User_name,Pass_word)

        for recipient in Contact_list:
            msg = EmailMessage()
            msg['Subject'] = "Test from CFL's email automation Assistant"
            msg['From'] = 'chufeng.li@cfel.de'
            msg['To'] = recipient
            msg.set_content(body)

            flist = glob.glob('./*.jpg')
            for file in flist:
                with open(file,'rb') as f:
                    file_data = f.read()
                    file_name = f.name
                    file_type = imghdr.what(f.name)
                    msg.add_attachment(file_data,maintype='image',subtype=file_type,filename=file_name)

            smtp.send_message(msg)
            print('The message sent to recipient %s !'%(recipient))
    return
if __name__=='__main__':
    # Contact_list = ['2541295710@qq.com','lightdrivencarbon@gmail.com',\
    # 'chu0518@qq.com','haohu3@asu.edu','xinyang.li@desy.de',\
    # 'xiao.sun@desy.de','ywang542@asu.edu','chufengl@icloud.com']
    Contact_list = ['chufengl@icloud.com']
    #Contact_list = ['2541295710@qq.com','chufengl@icloud.com']
    sending_time = datetime.datetime(2020,5,8,2,30,00)
    mail_auto_beta(Contact_list,sending_time)
