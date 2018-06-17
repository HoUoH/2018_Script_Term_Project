#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from http.client import HTTPSConnection
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback


key = '430156241533f1d058c603178cc3ca0e'
TOKEN = '538495097:AAHwYi7k1ftDxhXs8r-7hFIWdLJFoR-2C44'
MAX_MSG_LENGTH = 300
baseurl = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml?key="+key
bot = telepot.Bot(TOKEN)



def getTodayMovieData(date_param):

    res_list = []
    url = baseurl + '&targetDt=' + date_param
    # print(url)
    res_body = urlopen(url).read()
    #print(res_body.decode())
    soup = BeautifulSoup(res_body, 'html.parser')
    items = soup.findAll('dailyboxoffice')
    #items = soup.find_all('dailyboxoffice') #findAll dailyboxoffice


    for item in items:
        item = re.sub('<.*?>', '|', item.decode()) # <>의 내용, |로 구분하고, item의 text들을 갖고온다
        parsed = item.split('||')
        print(parsed)
        try:
            row =  parsed[1]+'위'+ '\n' + \
                  '제목 : '+parsed[6]+'\n' + \
                  '점유율 : '+parsed[9]+'%\n' + \
                  '당일 관객수 : '+parsed[13]+'\n' + \
                  '누적 관객수 : '+parsed[16]+'\n' + \
                  '-------------------------------------------'
        except IndexError:
            row = item.replace('||', '\n')

        if row:
            res_list.append(row.strip())
    return res_list

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run(date_param):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, date TEXT, PRIMARY KEY(user, date) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, date_param, param)
        res_list = getTodayMovieData( param, date_param )
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run(current_month)