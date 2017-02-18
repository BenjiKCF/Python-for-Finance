import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import bs4 as bs
import pickle
import requests
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

style.use('ggplot')

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text)
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(str(ticker))

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    print tickers
    return tickers

def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500 == True:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2000, 1, 1)
    end = dt.datetime(2016, 12, 31)

    for ticker in tickers:
        print ticker
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers):
        df = pd.read_csv('/Users/kachunfung/python/finance/stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace = True)

        df.rename(columns = {'Adj Close': ticker}, inplace = True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count % 10 == 0:
            print (count)

    print (main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')

def visualize_data():
    df = pd.read_csv('sp500_joined_closes.csv')
    #df['AAPL'].plot()
    #plt.show()
    df_corr = df.corr()

    print (df_corr)
    data = df_corr.values # inner value of the dataframe, no index, no header
    fig = plt.figure() # create a figure object
    ax = fig.add_subplot(1,1,1) # create an axes object in the figure,
    # number of rows, columns, and the ID of the subplot, between 1 and the number of columns times the number of rows.

    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn) #plot colour cmap = from Red to Yello to Green
    fig.colorbar(heatmap) # legend


    # put the major ticks at the middle of each cell
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    # set_xticks = Set the x ticks with list of ticks
    # arange = form an array
    # shape[0] = how many rows, shape[1] = how many columns
    # data.shape[0] = 505 rows
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)

    # want a more natural, table-like display
    ax.invert_yaxis() # top of matplotlib graph
    ax.xaxis.tick_top() # move xaxis tick to the top

    # set the labels
    column_labels = df_corr.columns
    row_labels = df_corr.index

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90) # rotating the label
    heatmap.set_clim(-1, 1) # limit of color
    plt.tight_layout() # clean things out, show better
    plt.show()

visualize_data()
