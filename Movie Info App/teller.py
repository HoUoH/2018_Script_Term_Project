#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

import noti

def getToday(): # 검색에 용이하게 현재 날짜 가져옴.
    now = datetime.now()

    if now.month / 10 <= 1:
        zeroMonth = '0' + str(now.month)
    else:
        zeroMonth = str(now.month)

    if now.day / 10 <= 1:
        zeroDay = '0' + str(now.day-1)
    else:
        zeroDay = str(now.day-1)

    today = str(now.year) + str(zeroMonth) + str(zeroDay)
    return today

date = str(getToday())

def TodayMovieData(user):   #초기값
    print(user, date)
    res_list = noti.getTodayMovieData(date)
    msg = ''
    for r in res_list:
        if r == res_list[0]:
            msg += "===== " + date + " =====\n"
        print( r )
        if len(r+msg)+1>noti.MAX_MSG_LENGTH:
            noti.sendMessage( user, msg )
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        noti.sendMessage( user, msg )


def replyMovieData(date_param, user):   #초기값
    print(user, date_param)
    res_list = noti.getTodayMovieData(date_param)
    msg = ''
    for r in res_list:
        if r == res_list[0]:
            msg += "===== " + date_param + " =====\n"
        print( r )
        if len(r+msg)+1>noti.MAX_MSG_LENGTH:
            noti.sendMessage( user, msg )
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        noti.sendMessage( user, msg )
    else:
        noti.sendMessage( user, '%s 기간에 해당하는 데이터가 없습니다.'%date_param )

def save( user, date_param ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, date TEXT, PRIMARY KEY(user, date) )')
    try:
        cursor.execute('INSERT INTO users(user, date) VALUES ("%s", "%s")' % (user, date_param))
    except sqlite3.IntegrityError:
        noti.sendMessage( user, '이미 해당 정보가 저장되어 있습니다.' )
        return
    else:
        noti.sendMessage( user, '저장되었습니다.' )
        conn.commit()

def check( user ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, date TEXT, PRIMARY KEY(user, date) )')
    cursor.execute('SELECT * from users WHERE user="%s"' % user)
    for data in cursor.fetchall():
        row = 'ID:' + str(data[0]) + ', 날짜:' + data[1]
        noti.sendMessage( user, row )


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('조회') and len(args) > 1:
        if (len(args[1]) is not 8):
            noti.sendMessage(chat_id, "날짜는 yyyymmdd형식 입니다.")
            return
        print('try to', args[1], '일자 박스오피스')
        replyMovieData(args[1], chat_id)
    elif text.startswith('저장') and len(args) > 1:
        if(len(args[1]) is not 8):
            noti.sendMessage(chat_id, "날짜는 yyyymmdd형식 입니다.")
            return
        print('try to 저장', args[1])
        save( chat_id, args[1])
    elif text.startswith('확인'):
        print('try to 확인')
        check( chat_id )
    elif text == '어제':
        print('try to 전날 박스오피스')
        TodayMovieData(chat_id)
    else:
        noti.sendMessage(chat_id,
'**** 모르는 명령어입니다. ****\n\n\
=========가능한 명령어=========\n\
1. 어제 \n\
└ 어제 박스오피스 정보조회\n\n\
2. 조회 yyyymmdd\n\
└ 해당일 박스오피스 정보조회\n\
└ [ex)조회 20180611]\n\n\
3. 저장 yyyymmdd\n\
└ 해당 날짜 저장\n\n\
4. 확인\n\
└ 저장된 날짜 확인')



#today = date.today()
#current_month = today.strftime('%Y%m')

#print( '[',today,']received token :', noti.TOKEN )

bot = telepot.Bot(noti.TOKEN)
pprint( bot.getMe() )

bot.message_loop(handle)

print('Listening...')

while 1:
  time.sleep(10)