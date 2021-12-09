# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 00:08:06 2021

"""

import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import alpaca_trade_api as tradeapi

from dotenv import load_dotenv
from pathlib import Path
import os


load_dotenv()
keyId     = os.getenv("keyId")
secretKey = os.getenv("secretKey")
endpoint  = os.getenv("endpoint")
api = tradeapi.REST(keyId, secretKey, endpoint)

account = api.get_account()

# Check if our account is restricted from trading.
if account.trading_blocked:
    print('Account is currently restricted from trading.')

# Check how much money we can use to open new positions.
print('${} is available as buying power.'.format(account.buying_power))

# Get daily price data for AAPL over the last 5 trading days.
stock = ['AAPL','VOO']
barset = api.get_barset(stock, 'day', limit=5)
aapl_bars = barset[stock[0]]
# See how much AAPL moved in that timeframe.
week_open = aapl_bars[0].o
week_close = aapl_bars[-1].c
percent_change = (week_close - week_open) / week_open * 100
print('{} moved {}% over the last 5 days'.format(stock, percent_change))

plt.figure()
plt.plot([aapl_bars[i].o for i in range(len(aapl_bars))], label='open')
plt.plot([aapl_bars[i].l for i in range(len(aapl_bars))], label='low')
plt.plot([aapl_bars[i].h for i in range(len(aapl_bars))], label='high')
plt.plot([aapl_bars[i].c for i in range(len(aapl_bars))], label='close')
plt.legend()
plt.savefig('moving_average.png')