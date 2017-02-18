import numpy as np
import pandas as pd
import pickle

# 7days, 2% up buy, 2% down sell

def process_data_for_labels(ticker):
    hm_days = 7 # how many days
    df = pd.read_csv('sp500_joined_closes.csv', index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)

    for i in range(1, hm_days+1):
        # '{}'.format = String formatting
        # up = -i = i days in future
        # (new - old) / old
        df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]

    df.fillna(0, inplace=True)
    return tickers, df

def buy_sell_hold(*args): # *args = any number of argument
    cols = [c for c in args] # list comprehension
    requirement = 0.02 # if stock price changes for 2%
    for col in cols:
        if col > requirement:
            return 1 # buy
        if col < -requirement:
            return -1 # sell
    return 0 # hold
