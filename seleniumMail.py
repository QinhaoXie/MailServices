from selenium import webdriver
from selenium.webdriver.common.by import By
import re,sys
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# driver = webdriver.Remote(

#   command_executor='http://127.0.0.1:4444/wd/hub',

#   desired_capabilities=DesiredCapabilities.CHROME)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument('--no-sandbox')  # fix:DevToolsActivePort file doesn't exist
options.add_argument('--disable-gpu')  # fix:DevToolsActivePort file doesn't exist
options.add_argument('--disable-dev-shm-usage')  # fix:DevToolsActivePort file doesn't exist
options.add_argument('--remote-debugging-port=9222')  # fix:DevToolsActivePort file doesn't
# driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', options=options)

driver = webdriver.Chrome(options=options)

driver.get('https://www.bangumi.app/hot/anime')

# s=driver.find_elements(By.XPATH,"/html/body/div/div/div[2]/div/div[2]")
# print(str(s.get_attribute('innerHTML')))

print(driver.title)
fh = open("111.html", encoding="utf-8",mode="w+")
fh.write("<head>  <meta charset=\"UTF-8\"></head>")
fh.writelines("""<style>
    .flex-container>div {
        background-color: #f1f1f1;
        width: 24%;
        margin: 5px;
        text-align: center;
        line-height: 45px;
        font-size: 20px;
    }
    img{
        width: 90%;
    }
    .flex-container{
        margin:auto;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        background-color: DodgerBlue;width:90%
    }
    .flex-container>div>div{
        word-wrap: normal;
              width:95%;
    }
     </style>         """)
ids=[]
srcs=[]
names=[]
infos=[]
for e in driver.find_elements(By.CLASS_NAME,"object-cover"):
    print(e.get_attribute('src'))
    print('-'*20)
    srcs.append(e.get_attribute('src'))
for e in driver.find_elements(By.CLASS_NAME,"w-52"):
    print([i.get_attribute('innerText') for i in e.find_elements(By.TAG_NAME,'div')])
    print('-'*20)
    names.append([i.get_attribute('innerText') for i in e.find_elements(By.TAG_NAME,'div')])
for e in driver.find_elements(By.CSS_SELECTOR," div.mt-1.flex.justify-between.py-1"):
    print(e.get_attribute('innerText'))
    print('-'*20)
    infos.append(e.get_attribute('innerText'))
for url in srcs:
    ids.append(re.search('\/(\d*)_',url).group(1))
title=names.pop(0)
print(ids,end="\n-----------------\n")
print(srcs,end="\n-----------------\n")
print(names,end="\n-----------------\n")
print(infos,end="\n-----------------\n")

print(range(len(srcs)))
print(range(len(names)))
print(range(len(infos)))

fh.write(title[0][4:])
fh.write("<div class=\"flex-container\">")
for i in range(len(srcs)):
    print(i)
    fh.write("<div style='background-color: #f1f1f1;'>")
    fh.write(f"<h2>**{i+1}**</h2>")
    fh.write(f"<img src={srcs[i]}>")
    fh.write(f"<div>{names[i][0]}</div>")
    fh.write(f"<div>{names[i][1]}</div>")
    fh.write(f"<div>{infos[i]}</div>")
    fh.write(f"<div><a href=\"https://bangumi.tv/subject/{ids[i]}\">details</a></div>")
    fh.write("</div>")
fh.write("</div>")
fh.close()
driver.quit()


fh2 = open('111.html',mode='r',encoding='utf-8')
Mailtext = fh2.readlines()
Mailtext = ''.join(Mailtext) 

fh2.close()








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


def sendnotice(sender,senderpass,my_receiver,text):
    my_sender = sender    # 发件人邮箱账号
    my_pass = senderpass              # 发件人邮箱密码
    print(text)
    def mail():
        ret=True
        try:
            msg=MIMEText(text,'html','utf-8')
            msg['From']=formataddr(["FromRunoob",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To']=formataddr(["FK",my_receiver])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject']="BANGUMI 热门动画"                # 邮件的主题，也可以说是标题
    
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
    sendnotice(sender,senderpass,my_receiver,Mailtext)
