# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 00:08:06 2021

"""
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from sklearn.linear_model import LinearRegression
from math import sqrt

import alpaca_trade_api as tradeapi

# MODIFIABLE GLOBAL VARS
days = 300 # Obtain 300 days worth of data
stocks = ['AAPL','VOO', 'NVDA', 'AMD', 'VHT']
#stocks = ['VOO']

# STATIC GLOBAL ENVIRONMENT VARIABLES
load_dotenv()
keyId     = os.getenv("keyId")
secretKey = os.getenv("secretKey")
endpoint  = os.getenv("endpoint")
api = tradeapi.REST(keyId, secretKey, endpoint)


# FUNCTIONS
def pythag(pt1, pt2):
    a_sq = (pt2[0] - pt1[0]) ** 2
    b_sq = (pt2[1] - pt1[1]) ** 2
    return sqrt(a_sq + b_sq)

def local_min_max(pts):
    local_min = []
    local_max = []
    prev_pts = [(0, pts[0]), (1, pts[1])]
    for i in range(1, len(pts) - 1):
        append_to = ''
        if pts[i-1] > pts[i] < pts[i+1]:
            append_to = 'min'
        elif pts[i-1] < pts[i] > pts[i+1]:
            append_to = 'max'
        if append_to:
            if local_min or local_max:
                prev_distance = pythag(prev_pts[0], prev_pts[1]) * 0.5
                curr_distance = pythag(prev_pts[1], (i, pts[i]))
                if curr_distance >= prev_distance:
                    prev_pts[0] = prev_pts[1]
                    prev_pts[1] = (i, pts[i])
                    if append_to == 'min':
                        local_min.append((i, pts[i]))
                    else:
                        local_max.append((i, pts[i]))
            else:
                prev_pts[0] = prev_pts[1]
                prev_pts[1] = (i, pts[i])
                if append_to == 'min':
                    local_min.append((i, pts[i]))
                else:
                    local_max.append((i, pts[i]))
    return local_min, local_max

def regression_ceof(pts):
    X = np.array([pt[0] for pt in pts]).reshape(-1, 1)
    y = np.array([pt[1] for pt in pts])
    model = LinearRegression()
    model.fit(X, y)
    return model.coef_[0], model.intercept_

def regression(aapl):
    key = 'Close'
    """
    plt.figure()

    aapl[key].plot()
    plt.title(key)
    """

    # Moving Average
    for i in range(5,20+1,5):
        column_name = "MA%s" %(str(i))
        aapl[column_name] = aapl[key].rolling(window=i,center=False).mean()
        # Plot rolling
        #aapl[column_name].plot()
    #plt.legend()
    #plt.savefig(f'{key}.png')

    # Smooth Function
    month_diff = days//30
    if month_diff == 0:
        month_diff = 1
    smooth = int(2 * month_diff + 3) # Simple algo to determine smoothness
    pts = savgol_filter(aapl['Close'], smooth, 3) # Get the smoothened price data

    """
    plt.figure()
    plt.title(stock)
    plt.xlabel('Days')
    plt.ylabel('Prices')
    plt.plot(pts, label=f'Smooth {stock}')
    plt.legend()
    plt.show()
    plt.savefig(f'{key}.png')
    """

    # Regression

    local_min, local_max = local_min_max(pts)

    local_min_slope, local_min_int = regression_ceof(local_min)
    local_max_slope, local_max_int = regression_ceof(local_max)

    pad = 50
    support = (local_min_slope * np.arange(days+pad)) + local_min_int
    resistance = (local_max_slope * np.arange(days+pad)) + local_max_int
    center = (support+resistance)/2

    plt.figure()

    aapl[key].plot()
    #plt.plot(pts, label=f'Smooth {stock}')
    plt.plot(support, label='Support y={0:.2f}x+{1:.2f}'.format(local_min_slope, local_min_int), c='r')
    plt.plot(resistance, label='Resistance', c='g')
    plt.plot(center)
    plt.scatter([i[0] for i in local_min],[i[1] for i in local_min] , c='r')
    plt.scatter([i[0] for i in local_max],[i[1] for i in local_max] , c='g')
    plt.title(stock+" " + str(aapl['Date'].iloc[-1]))
    plt.xlabel('Days')
    plt.ylabel('Prices')
    plt.legend()
    plt.show()
    plt.savefig(f'{stock}.png') 

# SCRIPTING
# Load Account
account = api.get_account()

# Check if our account is restricted from trading.
#if account.trading_blocked:
#    print('Account is currently restricted from trading.')

# Check how much money we can use to open new positions.
#print('${} is available as buying power.'.format(account.buying_power))

# Get daily price data for AAPL over the last X trading days.
barset = api.get_barset(stocks, 'day', limit=days)
for stock in stocks:
    bars = barset[stock]
    # See how much AAPL moved in that timeframe.
    week_open = bars[0].o
    week_close = bars[-1].c
    percent_change = (week_close - week_open) / week_open * 100
    print('{} moved {}% over the last {} days'.format(stock, percent_change,days))

    # View Data
    """
    plt.figure()
    plt.plot([bars[i].o for i in range(len(bars))], label='open')
    plt.plot([bars[i].l for i in range(len(bars))], label='low')
    plt.plot([bars[i].h for i in range(len(bars))], label='high')
    plt.plot([bars[i].c for i in range(len(bars))], label='close')
    plt.title('Open and Close')
    plt.legend()
    plt.savefig('apple_plot.png')
    """

    # Reorganize Data into dataframe
    aapl = pd.DataFrame({
        'Date':   [bars[i].t for i in range(len(bars))],
        'Volume': [bars[i].v for i in range(len(bars))], 
        'Open':   [bars[i].o for i in range(len(bars))],
        'High':   [bars[i].h for i in range(len(bars))],
        'Low':    [bars[i].l for i in range(len(bars))],
        'Close':  [bars[i].c for i in range(len(bars))],          
    })

    regression(aapl)

# Fibanocci
