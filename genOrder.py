import os
from datetime import datetime, timedelta

sd = datetime(year = 2019, month = 01, day = 01)
ed = datetime(year = 2019, month = 01, day = 12)
for i in range(int((ed - sd).days)):
	dt = sd + timedelta(i)
	os.system('python updateIns.py {}'.format(dt.strftime('%Y%m%d')))
	os.system('python updateIns.py {}'.format(dt.strftime('%Y%m%d')))
	os.system('python updateOrder.py EOS dy {}'.format(dt.strftime('%Y%m%d')))
	os.system('python updateOrder.py ETH eth {}'.format(dt.strftime('%Y%m%d')))