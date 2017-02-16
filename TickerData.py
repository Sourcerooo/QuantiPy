import bs4 as bs
import datetime as dt
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import pandas_datareader as web
import pickle
import requests
import data_base as db


def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers=[]
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    with open("./Data/sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    print(tickers)
    return tickers

def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("./Data/sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists('./Data/stock_dfs'):
        os.makedirs('./Data/stock_dfs')

    startdate = dt.datetime(2000, 1, 1)
    enddate = dt.datetime(2016, 12, 31)

    for ticker in tickers:
        print(ticker)
        if not os.path.exists('./Data/stock_dfs/{}.csv'.format(ticker)):
            try:
                df = web.DataReader(ticker, 'yahoo', startdate, enddate)
                df.to_csv('./Data/stock_dfs/{}.csv'.format(ticker))
            except Exception as e:
                print(e)
        else:
            print('Already have ticker {}'.format(ticker))


def compile_data():
    with open("./Data/sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers):
        try:
            df = pd.read_csv("./Data/Stock_dfs/{}.csv".format(ticker))
            df.set_index('Date', inplace=True)

            df.rename(columns={'Adj Close': ticker}, inplace=True)
            df.drop(["Open", "High", "Low", "Close", "Volume"], 1, inplace=True)

            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df, how='outer')

        except Exception as e:
            print(e)

        if count % 10 == 0:
            print(count)

    print(main_df.head)
    main_df.to_csv("./Data/Stock_dfs/joined_close_data.csv")


def visualize_data():
    style.use("ggplot")
    df = pd.read_csv("./Data/Stock_dfs/joined_close_data.csv")
    #Calculate correlation between assets
    df_corr = df.corr()
    print(df_corr.head())

    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns
    row_labels = df_corr.index

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1, 1)
    plt.tight_layout()
    plt.show()

    #df["AAPL"].plot()
    #plt.show()
    # print(df["AAPL"])


print(str(db._conn))
db.open_database("test.db")
print(str(db._conn))
db.close_database()

# db.create_table()
# db.data_entry()
#db.create_new_table(tablename="MyNewTable",field_type_tupel=[("field1", "TEXT"), ("field2", "REAL"), ("field3", "TEXT"), ("field4", "REAL")])

#visualize_data()
# compile_data()
# get_data_from_yahoo()
# save_sp500_tickers()