from gettext import find
from lzma import FORMAT_ALONE
from urllib import response
import requests
from bs4 import BeautifulSoup
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket

now = datetime.datetime.now()

content=''

def extract_news(url):
    print('Extracting News headlines...')
    cnt=''
    cnt+=('<b>Hn Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')
    response=requests.get(url)
    content=response.content
    soup=BeautifulSoup(content,'html.parser')
    for i, tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})):
        cnt+=((str(i+1)+'::'+tag.text+"\n"+'<br>') if tag.text!='More' else'')
    return cnt

cnt=extract_news('https://news.ycombinator.com')
content+=cnt
content+=('<br>------------<br>')
content+=('<br><br>End of news')

#Email

print('Composing Email...')

#my email data
SERVER='fzglanjltdevacpruw@nthrw.com'#your smtp server
PORT='587'#your port number
FROM='tathagat.gaur201@gmail.com'#your from email id
TO='tathagat.gaur201@gmail.com'#your to email ids
PASS='tathagatgaur201'#your email ids password

socket.getaddrinfo('localhost', 25)

#fp=open(file_name.rb)
#Create a text/plain
#msg=MIMEtext('')
msg=MIMEMultipart()

msg['Subject']='Top news stories HN[Automated Email]'+' '+str(now.day)+'-'+str(now.month)+'-'+str(now.year)
msg['From']=FROM
msg['TO']=TO

msg.attach(MIMEText(content,'html'))
#fp close

print('Intializing server....')
server=smtplib.SMTP(SERVER,PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM,PASS)
server.sendmail(FROM,TO,msg.as_string())
print('Email sent')

server.quit()