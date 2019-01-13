import json
import sys
import pandas as pd
import os
from pytz import timezone
#root_dir = '/Users/apple/Documents/trading/' #dev
root_dir = '/root/' #prod
sys.path.append(root_dir + 'trading')
from func import *
from datetime import datetime, date, time, timedelta