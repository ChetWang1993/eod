#!/usr/local/bin/python
# encoding: UTF-8
import time
#import datetime
from datetime import datetime
#from func import *
from binance.client import Client
from datetime import timedelta
import sys
import os
import pandas as pd
from vnpy.trader.app.ctaStrategy.ctaBase import MINUTE_DB_NAME
from vnpy.trader.app.ctaStrategy.ctaHistoryData import loadMcCsv


if len(sys.argv) != 4:
    print("usage: {} symbol sd ed".format(sys.argv[0]))
    quit()
# 将时间戳转化为标准时间
def to_localtime(strap):
    time_local = time.localtime(strap)
    dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
    return dt

symbol = '{}USDT'.format(sys.argv[1])
sd = datetime.strptime(sys.argv[2], '%Y%m%d')
ed = datetime.strptime(sys.argv[3], '%Y%m%d')

data_dir = '../data/bt/BINANCE/{}/spot/'
filename = '{}.csv'
interval = Client.KLINE_INTERVAL_1MINUTE        # K线的时间间隔

APIkey = 'R0546VwwTnhBNXdxi9a9Z7dkRHnCP8DyY0ah8KTDClxZqEOBaFkKgYLTLF8Acow8'
Secretkey = 'J72JCQIxm3RRFDIwFXNWnSlmgKadEqaz184j2sjSeBGLBu9dDZ7kB7ImPR6Jdgqx'
client = Client(APIkey, Secretkey)

for d in [sd + timedelta(x) for x in range(int((ed - sd).days))]:
    s_dir = data_dir.format(symbol)
    td = d.strftime('%d %b, %Y')
    tmr = (d + timedelta(1)).strftime('%d %b, %Y')
    # start = "17 Jul, 2018"       # 开始时间
    # end = "17 Sep, 2018"        # 结束时间
    klines = client.get_historical_klines(symbol, interval, td, tmr)      # 获取 K 线
    klines = klines[:-1]
    df = pd.DataFrame([{'Date': to_localtime(x[0]/1000).split(' ')[0], 
        'Time': to_localtime(x[0]/1000).split(' ')[1],
        'High': str(x[2]), 'Low': str(x[3]), 
        'Open': str(x[1]), 'Close': str(x[4]), 
        'TotalVolume': '{}.{}'.format(str(x[5]).split('.')[0], str(x[5]).split('.')[1])} for x in klines])
    #print(df)

    if not os.path.exists(s_dir):
        os.makedirs(s_dir)

    df.to_csv(s_dir + filename.format(d.strftime('%Y%m%d')), index=False)
    loadMcCsv(s_dir + filename.format(d.strftime('%Y%m%d')), MINUTE_DB_NAME, symbol)

    # 比对官网数据，发现返回值前六项的含义以及对应顺序：时间戳，开，高，低，收，量
    # with open(data_folder.format(symbol, dt), 'w') as f:
    #     f.write('Timestamp,datetime,symbol,high,low,open,close,volume')
    #     f.write('\n')
    #     for element in klines:
    #         real_stamp = element[0]/1000        # 观察发现币安时间戳其实是1000倍的时间戳
    #         real_time = to_localtime(real_stamp)       # 转化为标准时间
    #         f.write(str(real_stamp) + ',' + str(real_time) + ',' + symbol + ',' + str(element[2]) + ',' + str(element[3]) + ',' + str(element[1]) + ',' + str(element[4]) + ',' + str(element[5]))
    #         f.write('\n')