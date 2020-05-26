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
import mimetypes
import yaml

def mail_auto_beta(Contact_list,sending_time):
    User_name = 'lichufen'
    Pass_word = os.environ.get('Email_password')
    Host_name = 'smtp-auth.desy.de'


    body = '''熊主人：
这封邮件是熊主人的小黄人管家发的，是提醒你叫他起床的。
*****
小黄人，敬上！
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

def mail_dict_list_sort_key(mail_dict):
    key = mail_dict['sending_time']
    return key

def send_folders(parent_path):
    '''
    '''

    parent_path = os.path.abspath(parent_path)
    folder_list = glob.glob(os.path.join(parent_path,'mail*'))
    mail_dict_list = []
    for fd in folder_list:
        if not os.path.isdir(fd):
            continue
        if not os.path.isfile(os.path.join(fd,'conf.yml')):
            continue
        with open(os.path.join(fd,'conf.yml'),'r') as mail_f:
            mail_dict = yaml.load(mail_f,Loader=yaml.FullLoader)
            mail_dict['path'] = fd
            mail_dict['sending_time'] = datetime.datetime.strptime(mail_dict['sending_time'],'%Y %m %d %H:%M:%S')
            mail_dict_list.append(mail_dict)

    mail_dict_list.sort(key=mail_dict_list_sort_key) #sort() for list is an in-place method
    mail_dict_list = [m for m in mail_dict_list if mail_dict_list_sort_key(m)>datetime.datetime.now()]# filter the mails
    # with the sending time in the past.
    for mail_dict in mail_dict_list:

        msg = EmailMessage()
        msg['Subject'] = mail_dict['Subject']
        msg['From'] = 'chufeng.li@cfel.de'
        #msg['To'] = mail_dict['To']+', '+mail_dict['Cc']+', '+mail_dict['Bcc']
        msg['To'] = mail_dict['To']
        if 'Cc' in mail_dict:
            msg['Cc'] = mail_dict['Cc']
        if 'Bcc' in mail_dict:
            msg['Bcc'] = mail_dict['Bcc']
        msg.set_content(mail_dict['Body']) # plain text part

        file_list = glob.glob(os.path.join(mail_dict['path'],mail_dict['attachment']))
        file_list = [m for m in file_list if not m.endswith('.yml')]


        for file in file_list:
            if not os.path.isfile(file):
                continue
            ctype, encoding = mimetypes.guess_type(file)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            with open(file, 'rb') as fp:
                msg.add_attachment(fp.read(),
                               maintype=maintype,
                               subtype=subtype,
                               filename=os.path.basename(file))

        User_name = 'lichufen'
        Pass_word = os.environ.get('Email_password')
        Host_name = 'smtp-auth.desy.de'

        while datetime.datetime.now() < mail_dict['sending_time']:
            delta = mail_dict['sending_time'] - datetime.datetime.now()
            print('time left: %s'%(str(delta)))
            time.sleep(5)
        with smtplib.SMTP(Host_name,587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(User_name,Pass_word)
            smtp.send_message(msg)
        print('The message: \n%s \nhas been sent to recipient:\n %s !'%(mail_dict['Subject'],mail_dict['To']))


    return

if __name__=='__main__':
    ################################################################
    parent_path = os.path.abspath(sys.argv[1])
    send_folders(parent_path)
    ################################################################
