#!/usr/local/bin/python
# encoding: UTF-8
from constantsEOD import *
import glob

if len(sys.argv) < 2:
	print('usage: {} strat [dt]'.format(sys.argv[0]))
	quit()

if len(sys.argv) == 3:
	dt = sys.argv[2]
else:
	dt = datetime.now().strftime('%Y%m%d')

strat = sys.argv[1]
pnl_dir = root_dir + 'eod/data/pnl/{}/'.format(strat)
pnl = 0.0
conf_path = root_dir + 'trading/conf/OKEX_{}.json'
dt_format = '%Y%m%d'
pnl_ks = ['timestamp', 'equity', 'avail_balance', 'spot_balance', 'cash', 'transfer']

setting = json.load(open(conf_path.format(strat)))

pnls = pd.DataFrame(columns = pnl_ks)

fs = [x.split('/')[-1].split('.')[0] for x in list(glob.glob(pnl_dir.format(strat) + '*.txt'))]
dt = datetime.strptime(max(fs), dt_format)
sd = dt - timedelta(6)
ed = dt

for x in range(int((ed - sd).days)):
	x_dt = (sd + timedelta(x)).strftime(dt_format)

	#x_dt = x.split('/')[-1].split('.')[0]
	pnls = pnls.append(pd.read_csv(pnl_dir + '{}.txt'.format(x_dt), sep='\t'), sort=False)

print(pnls.iloc[-1].equity - pnls.iloc[0].equity)
# BUY = '1'
# SELL = '3'
# SHORT = '2'
# COVER = '4'

# if orders.iloc[0]['type'] in [3, 4]:
# 	orders = orders[1:]
# orders = orders.reset_index().drop(['index'], axis = 1)[:len(orders) - len(orders) % 2]
# print(orders)

# for (idx1, row1), (idx2, row2) in zip(orders[:-1].iterrows(), orders[1:].iterrows()):
# 	if not idx1 % 2:
# 		if row1['size'] != row2['size']:
# 			print(row1); print(row2); print('[ERROR]: order size different')
# 			quit()

# 		row1['size'] * 10 / 
# 		if row1['type'] == 1 and row2['type'] == 3:
# 			pnl += row1['size'] * (row2['price_avg'] - row1['price_avg'])
# 		elif row1['type'] == 2 and row2['type'] == 4:
# 			pnl += row1['size'] * (row1['price_avg'] - row2['price_avg'])
# 		else:
# 			print(row1); print(row2); print('[ERROR]: order type not match')
# 			quit()
# 		pnl -= row1['fee']
# 		pnl -= row2['fee']

# print(pnl)
