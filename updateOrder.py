#!/usr/local/bin/python
# encoding: UTF-8
import json
import sys
import pandas as pd
sys.path.append('../trading')
from func import *
from datetime import datetime, date, time, timedelta

if len(sys.argv) < 3:
	print('usage: {} symbol strat [dt]'.format(sys.argv[0]))
	quit()

#root_dir = '/Users/apple/Documents/trading/'
root_dir = '/root/'
order_path = root_dir + 'eod/data/order/{}/{}.txt'
eod_path = root_dir + 'eod/data/instrument/{}.txt'
ts_format = '%Y-%m-%dT%H:%M:%S.%fZ'
conf_path = root_dir + 'trading/conf/OKEX_{}.json'
symbol = sys.argv[1]
strat = sys.argv[2]

if len(sys.argv) == 4:
	dt = sys.argv[3]
else:
	dt = datetime.now().strftime('%Y%m%d')
yd = (datetime.strptime(dt, '%Y%m%d') - timedelta(1)).replace(hour=0, minute=0, second=0, microsecond=0)
td = datetime.strptime(dt, '%Y%m%d').replace(hour=0, minute=0, second=0, microsecond=0)

setting = json.load(open(conf_path.format(strat)))

okApi = okApi(setting['apiKey'], setting['secretKey'],
	setting['order_log_dir'].format(setting['symbol']) + setting['order_log_name'].format(datetime.now()))
[instrument] = [x.rstrip() for x in list(open(eod_path.format(dt)).readlines()) if symbol in x]

try:
	ret = okApi.get_okex('/api/futures/v3/orders/{}?status=7'.format(instrument))

	ks = ['instrument_id', 'size', 'timestamp', 'filled_qty', 'fee', 'order_id', 'price', 'price_avg',
		'status', 'type', 'contract_val', 'leverage']
	orders = [dict(zip(ks, [x['instrument_id'], x['size'],
		datetime.strptime(x['timestamp'],
			ts_format).replace(tzinfo=timezone('GMT')).astimezone(timezone('Asia/Singapore')).strftime(ts_format),
		x['filled_qty'], x['fee'], x['order_id'], x['price'], x['price_avg'], x['status'], 
		x['type'], x['contract_val'], x['leverage']])) 
		for x in ret['order_info']]

	orders = [x for x in orders if datetime.strptime(x['timestamp'], ts_format) <= td and
		datetime.strptime(x['timestamp'], ts_format) >= yd]
	orders_yd = pd.DataFrame(orders)

	orders_yd.to_csv(order_path.format(strat, dt), index = False, sep = '\t')
except Exception as e:
	print('[ERROR]: fail to generate order log for strat {} on {} because {}'.format(strat, dt, e))
print('[INFO]: generate order log for strat {} on {} successfully'.format(strat, dt))