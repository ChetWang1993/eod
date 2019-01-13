from constantsEOD import *

if len(sys.argv) < 2:
	print('usage: {} strat'.format(sys.argv[0]))
	quit()

strat = sys.argv[1]
pnl = pd.read_csv('../trading/log/pnl_{}.log'.format(strat), sep='\t')
pnl_dir = root_dir + 'eod/data/pnl/{}/'.format(strat)

sd = datetime(year = 2018, month = 11, day = 11)
ed = datetime(year = 2019, month = 01, day = 07)
ts_format = '%Y-%m-%dT%H:%M:%S.%fZ'

for x in range(int((ed - sd).days)):
	x_sd = (sd + timedelta(x))
	x_ed = x_sd + timedelta(1)
	pnl['timestamp'] = pd.to_datetime(pnl['timestamp'])
	x_df = pnl[(pnl['timestamp'] >= x_sd) & (pnl['timestamp'] <= x_ed)]
	x_df.loc[:, 'transfer'] = 0.0
	x_df.loc[:, 'spot_balance'] = 0.0
	x_df.to_csv(pnl_dir + '{}.txt'.format(x_sd.strftime('%Y%m%d')), index=False, sep='\t')
