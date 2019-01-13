from constantsEOD import *

if len(sys.argv) < 2:
	print('usage: {} strat'.format(sys.argv[0]))
	quit()

strat = sys.argv[1]
conf_path = root_dir + 'trading/conf/OKEX_{}.json'
pnl_dir = root_dir + 'eod/data/pnl/{}/'.format(strat)
ts_format = '%Y-%m-%dT%H:%M:%S.%fZ'

dt = datetime.now().strftime('%Y%m%d')
pnl_ks = ['timestamp', 'equity', 'avail_balance', 'spot_balance', 'cash', 'transfer']

pnl_path = pnl_dir.format(strat) + '{}.txt'.format(dt)

if not os.path.exists(pnl_dir):
	os.makedirs(pnl_dir)

if os.path.exists(pnl_path):
	pnl = pd.read_csv(pnl_path, sep = '\t')
else:
	pnl = pd.DataFrame(columns = pnl_ks)

setting = json.load(open(conf_path.format(strat)))
okApi = okApi(setting['apiKey'], setting['secretKey'], '')

try:
	res1 = okApi.get_okex("/api/futures/v3/accounts/" + setting['currency'])
	res2 = okApi.get_okex("/api/spot/v3/instruments/{}-USDT".format(setting['currency'].upper()) + "/ticker")
	spot_res = okApi.get_okex('/api/spot/v3/accounts/{}'.format(setting['currency']))
	pnl_value = [datetime.strptime(res2['timestamp'],
			ts_format).replace(tzinfo=timezone('GMT')).astimezone(timezone('Asia/Singapore')).strftime(ts_format),
		res1['equity'], res1['total_avail_balance'], spot_res['balance'], 
		(float(res1['equity']) + float(spot_res['balance'])) *float(res2['last']),
		0]

	pnl = pnl.append([dict(zip(pnl_ks, pnl_value))])
	pnl.to_csv(pnl_path, index = False, sep = '\t')
	print('[INFO]: generate pnl for strat {} on {} successfully'.format(strat, dt))
except Exception as e:
	print('[ERROR]: update pnl error\t{}'.format(e))
