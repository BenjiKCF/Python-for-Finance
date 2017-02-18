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
        # up = -i = i days in future
        # (new - old) / old
        df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]

    df.fillna(0, inplace=True)
    return tickers, df

print process_data_for_labels('XOM')
