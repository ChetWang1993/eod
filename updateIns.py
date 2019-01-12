#!/usr/local/bin/python
# encoding: UTF-8

import json
import sys
import pandas as pd
sys.path.append('../trading')
from func import *
from datetime import datetime, date, time, timedelta

#root_dir = '/Users/apple/Documents/trading/'
root_dir = '/root/'
strat = 'dy'
ts_format = '%y%m%d'
conf_path = root_dir + 'trading/conf/OKEX_{}.json'
ins_path = root_dir + 'eod/data/instrument/{}.txt'

setting = json.load(open(conf_path.format(strat)))

if len(sys.argv) == 2:
	dt = sys.argv[1]
else:
	dt = datetime.now().strftime('%Y%m%d')

okApi = okApi(setting['apiKey'], setting['secretKey'],
	setting['order_log_dir'].format(setting['symbol']) + setting['order_log_name'].format(datetime.now()))

try:
	ret = okApi.get_okex('/api/futures/v3/instruments')

	ins_list = {}

	for x in ret:
		if (not x['underlying_index'] in ins_list.keys()) or datetime.strptime(x['instrument_id'].split('-')[2], 
			ts_format) > datetime.strptime(ins_list[x['underlying_index']].split('-')[2], ts_format):
			ins_list[x['underlying_index']] = x['instrument_id']

	f = open(ins_path.format(dt), 'w')
	f.writelines([x + '\n' for x in ins_list.values()])
	print('[INFO]: generate instrument log for strat {} on {} successfully'.format(strat, dt))
except Exception as e:
	print('[ERROR]: fail to generate instrument log for strat {} on {} because {}'.format(strat, dt, e))