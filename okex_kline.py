#!/usr/local/bin/python
# --*-- encoding: utf-8 --*--
from constants import *

startTime = (datetime.now() - timedelta(3)).replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
endTime = (datetime.now() - timedelta(1)).replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
params = {'start': startTime, 'end': endTime, 'granularity': '60'}
okApi = okApi('f4437433-0378-4535-8ba6-1fdffce6cea5', '589CCC3715DE217F935343DD2F4EE06E', '')
res = okApi.get_okex("/api/futures/v3/instruments/" + 'EOS-USD-190329' + "/candles", params)
print([datetime.fromtimestamp(x[0]/1000) for x in res])