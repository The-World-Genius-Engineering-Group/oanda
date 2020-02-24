import requests
from urllib.request import urlopen
from urllib.error import HTTPError
import urllib.request as urlreq
from bs4 import BeautifulSoup as bs
import time
import re

Token=input("please enter your token number:")



def check(url):
    try:
        html=urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    try:
        bsobj=bs(html,"lxml")
    except AttributeError as e:
        return None
    return bsobj#この他、探しに行ったタグがなければNoneを返すのを付けるべき。

def get_news():
    url="https://www.reuters.com/theWire"
    bsobj=check(url)
    for link in bsobj.findAll("a",href=re.compile("https://www.reuters.com/article/"),limit=1):
        if "href" in link.attrs:
            a=(link.attrs["href"])
            a=a.split()
            a=set(a)
            for i in a:
                bsobj2=check(i)
                for head in bsobj2.find_all(class_="ArticleHeader_headline"):
                    head=head.string
                    title.append(head)
                for text in bsobj2.find_all(class_="StandardArticleBody_body"):
                    for l in text:
                        context.append(l.get_text())

def go_line(Token,title,context):
    message = '\r\n' + 'recently news' + str(title) + '\r\n'+"its context" +str(context) +'\r\n'
    #LINEで送信するメッセージを作成
    url2 = "https://notify-api.line.me/api/notify"
    #LINE Notify APIのURLを取得
    #自分のLINEアカウントのアクセストークンを取得
    headers = {"Authorization" : "Bearer "+ Token}
    #リクエストヘッダの指定
    payload = {"message" :  message}
    #メッセージデータの格納
    r2 = requests.post(url2 ,headers = headers ,data=payload)
    #メッセージの送信

title=[]
context=[]

def final():
    while True:
        get_news()
        go_line(Token,title,context)
        title.clear()
        context.clear()
        time.sleep(60)
        continue
