import requests
import sys

rep=requests.get("https://economia.awesomeapi.com.br/last/USD-CNY,USD-AUD")
USDCNY=rep.json()["USDCNY"]["bid"]
USDAUD=rep.json()["USDAUD"]["bid"]
print(USDCNY)
print(USDAUD)
print(float(USDCNY)/float(USDAUD))

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

def readconfs(confpath):
    a=open(confpath,'r')
    t=a.readlines()

    for s in t:
        if s.startswith("sender:"):
            #print(s.split("sender:")[1].rstrip())
            sender=(s.split("sender:")[1].rstrip())
        if s.startswith("senderpass:"):
            #print(s.split("senderpass:")[1].rstrip())
            senderpass=(s.split("senderpass:")[1].rstrip())
        if s.startswith("receivers:"):
            print("send to :",s.split("receivers:")[1].rstrip().split(","))
            receivers=(s.split("receivers:")[1].rstrip().split(","))
    return sender,senderpass,receivers

def sendnotice(sender,senderpass,my_receiver):
    my_sender = sender    # 发件人邮箱账号
    my_pass = senderpass              # 发件人邮箱密码
    def mail():
        ret=True
        try:
            msg=MIMEText(f'今天的汇率为：{float(USDCNY)/float(USDAUD)} RMB/AUD','plain','utf-8')
            msg['From']=formataddr(["FromRunoob",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To']=formataddr(["FK",my_receiver])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject']="汇率提醒"                # 邮件的主题，也可以说是标题
    
            server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender,[my_receiver,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            ret=False
        return ret
    
    ret=mail()
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")
path = "/".join(sys.argv[0].split("/")[:-1])
if path == '':
    path+='.'
sender,senderpass,receivers = readconfs(path+"/sender.conf")
for receiver in receivers:
    my_receiver=receiver
    sendnotice(sender,senderpass,my_receiver)
