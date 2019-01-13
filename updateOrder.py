#!/usr/local/bin/python
# encoding: UTF-8
from constantsEOD import *

if len(sys.argv) < 2:
	print('usage: {} strat [dt]'.format(sys.argv[0]))
	quit()

order_path = root_dir + 'eod/data/order/{}/{}.txt'
ins_path = root_dir + 'eod/data/instrument/{}.txt'
ts_format = '%Y-%m-%dT%H:%M:%S.%fZ'
conf_path = root_dir + 'trading/conf/OKEX_{}.json'
strat = sys.argv[1]

if len(sys.argv) == 3:
	dt = sys.argv[2]
else:
	dt = datetime.now().strftime('%Y%m%d')
nd = (datetime.strptime(dt, '%Y%m%d') + timedelta(1)).replace(hour=0, minute=0, second=0, microsecond=0)
td = datetime.strptime(dt, '%Y%m%d').replace(hour=0, minute=0, second=0, microsecond=0)

setting = json.load(open(conf_path.format(strat)))

okApi = okApi(setting['apiKey'], setting['secretKey'], '')
[instrument] = [x.rstrip() for x in list(open(ins_path.format(dt)).readlines()) if setting['currency'].upper() in x]

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

	orders_yd = pd.DataFrame(columns = ['contract_val', 'fee', 'filled_qty', 'instrument_id',
		'leverage', 'order_id', 'price', 'price_avg', 'size', 'status', 'timestamp', 'type'])
	orders = [x for x in orders if datetime.strptime(x['timestamp'], ts_format) <= nd and
		datetime.strptime(x['timestamp'], ts_format) >= td]

	if len(orders):
		orders_yd = orders_yd.append(orders)
	orders_yd.to_csv(order_path.format(strat, dt), index = False, sep = '\t')
	print('[INFO]: generate order log for strat {} on {} successfully'.format(strat, dt))
except Exception as e:
	print('[ERROR]: fail to generate order log for strat {} on {} because {}'.format(strat, dt, e))