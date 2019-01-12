sys.path.append('../trading')
import json
from func import *
from datetime import datetime, date, time, timedelta

if len(sys.argv) < 3:
	print('usage: {} symbol strat [dt]'.format(sys.argv[0]))
	quit()

order_dir = '/root/data/order/{}'
eod_dir = '/root/data/eod/{}'
td = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S`Z")
conf_path = '/Users/apple/Documents/conf/OKEX_{}.json'

if len(sys.argv) == 3:
	dt = sys.argv[3]
else:
	dt = datetime.now().strftime('%Y%m%d')
setting = json.load(conf_path.format(strat))
symbol = sys.argv[1]
okApi = okApi(okApi(setting['apiKey'], setting['secretKey'], 
	setting['order_log_dir'].format(setting['symbol']) + setting['order_log_name'].format(datetime.now()))
[instrument] = [x for x in list(open(eod_dir.format(dt)).readlines()) if symbol in x]

params = {'status': 7, 'instrument_id': instrument}
ret = okApi.get_okex('/api/futures/v3/orders/{}'.foramt(instrument), params)
ks = ['instrument_id', 'size', 'timestamp', 'filled_qty', 'fee', 'order_id', 'price', 'price_avg',
	'status', 'type', 'contract_val', 'leverage']
orders = [dict(zip(ks, [x['instrument_id'], x['size'], 
	datetime.strptime(x['timestamp'], '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=timezone('GMT')).astimezone(timezone('Asia/Singapore')),
	x['filled_qty'], x['fee'], x['order_id'], x['price'], x['price_avg'], x['status'], 
	x['type'], x['contract_val'], x['leverage']])) 
	for x in ret['order_info']]
orders = [x for x in x if datetime.strptime(x['timestamp'], '%Y-%m-%dT%H:%M:%S.%f') <= td]
orders_yd = pd.DataFrame(orders)
print(orders_yd)