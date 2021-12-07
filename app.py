# -*- coding: utf-8 -*-
'''
@date: 2021-10-29
@author: Yuxuan Lu, Li Jinxing, Chu Yumo
'''
import requests
import json
import urllib.parse
import smtplib
from os import environ
from email.mime.text import MIMEText

EMAIL_USERNAME = environ['EMAIL_USERNAME']
EMAIL_TO = environ['EMAIL_TO']
EMAIL_FROM = environ['EMAIL_FROM']
EMAIL_PASSWORD = environ['EMAIL_PASSWORD']
EMAIL_SERVER = environ['EMAIL_SERVER']
EMAIL_PORT = int(environ['EMAIL_PORT'])
core = json.loads(environ['DATA'])


result = ""

URL_SESSION = 'http://xgxt.bjut.edu.cn/nonlogin/qywx/authentication.htm?appId=2c95de297d4f8bfa017d8631748b7fe2&urlb64=L3dlYkFwcC94dWVnb25nL2luZGV4Lmh0bWwjL2FjdGlvbi9iYXNlSW5kZXgvJUU3JUE3JUJCJUU1JThBJUE4JUU1JUFEJUE2JUU1JUI3JUE1'
URL_CLOCKIN = 'http://xgxt.bjut.edu.cn/syt/zzapply/operation.htm'

# Part1 Get session
HEADER_SESSION = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'Connection': 'keep-alive',
    'X-Requested-With': 'com.tencent.wework',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; GM1910 Build/RKQ1.201022.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/95.0.4638.74 Mobile Safari/537.36 wxwork/3.1.7 MicroMessenger/7.0.1 NetType/4G Language/zh Lang/zh'
}

s = requests.Session()
s.cookies.set('id', core['id'])
s.cookies.set('token', core['token'])

response = s.get(URL_SESSION, headers=HEADER_SESSION)
print(response)
print(response.text)
print(response.headers)
if response.status_code != 200:
    result += "打卡失败！错误：获取session失败" + str(response.status_code)
    result += response.text
    
# Part2 Get header & data
HEADER = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://xgxt.bjut.edu.cn',
    'Referer': 'http://xgxt.bjut.edu.cn/webApp/xuegong/index.html',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; GM1910 Build/RKQ1.201022.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/95.0.4638.74 Mobile Safari/537.36 wxwork/3.1.7 MicroMessenger/7.0.1 NetType/4G Language/zh Lang/zh',
    'X-Requested-With': 'XMLHttpRequest',
}

# user info
info = {
    'xmqkb': {
        'id': '2c95de297d4f8bfa017d85f53d267613'
    },
    'c15': core['c15'],
    'c16': core['c16'],
    'c17': core['c17'],
    'c18': core['c18'],
    'type': 'YQSJSB',
    'location_longitude': core['location_longitude'],
    'location_latitude': core['location_latitude'],
    'location_address': core['location_address']
}

# suffix info (static)
suffix_raw = '&msgUrl=syt%2Fzzapply%2Flist.htm%3Ftype%3DYQSJSB%26xmid%3D402880c97b1c114b017b1c2af13d02d8&uploadFileStr=%7B%7D&multiSelectData=%7B%7D&type=YQSJSB'
# prefix info (user info mostly)
prefix_data = json.dumps(info, ensure_ascii=False)
prefix_raw = 'data='+urllib.parse.quote_plus(prefix_data)
DATA = prefix_raw + suffix_raw

# Part3 Clock in
response_clockin = s.post(url=URL_CLOCKIN, headers=HEADER, data=DATA)
print(response_clockin)
print(response_clockin.text)
print(response_clockin.headers)
# result = '打卡失败'

if response_clockin.text == 'success':
    result += '打卡成功'
else:
    if response_clockin.text == 'Applied today':
        result += '今天已经打过卡'
    else:
        result += f'''
HTTP status: {response_clockin.status_code}
打卡数据:
{
    json.dumps(info, ensure_ascii=False, sort_keys=True, indent=2)
}
'''
print(result)
message = MIMEText(result, 'plain', 'utf-8')
message['Subject'] = '打卡结果'
message['FROM'] = EMAIL_FROM
message['To'] = EMAIL_TO

server = smtplib.SMTP(EMAIL_SERVER)
server.connect(EMAIL_SERVER, EMAIL_PORT)
server.ehlo()
server.starttls()
server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
server.sendmail(EMAIL_USERNAME, [EMAIL_USERNAME], message.as_string())
