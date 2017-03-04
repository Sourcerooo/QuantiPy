#ds.convert_optionvue_csv("./Data/OptionVue/20150105.csv")



#imp_ov = conv.OptionVueImport()
#stock_data, future_date, option_date = imp_ov.import_data(filename="./Data/OptionVue/20150106.csv")
#print(option_date)

# stocks, futures, options = imp_ov.import_csv("./Data/OptionVue/20150106.csv")
#
# for stock in stocks:
#     print(stock)

# imp_yahoo = di.YahooStockImport()
# yhdf = imp_yahoo.import_data(stock_symbol=["AAPL","BA","C"], from_date="2010-05-01", to_date="2010-05-05")
# yhdf.set_index(["date","symbol"],inplace=True)
# from quantipy.basics.data_struct import StocksData
# import datetime
# yhdf.sort_index()

# for date, new_df in yhdf.groupby(level=0):
#     print("Date: {}".format(date))
#     for symbol, data in new_df.loc[date].iterrows():
#         #dn = dn.append(yhdf[date,symbol])
#         #print(yhdf.loc[date,symbol])
#         #dn.loc[(symbol, date)] = pd.DataFrame(data)
#         print("   Symbol: {}  Open: {}".format(symbol, data["open"]))
#
# print(dn)
#for (symbol, date), data in yhdf.iterrows():
#    print("Sym: {}  Date: {} Data: {} ".format(symbol, date, data["open"]))



# stock = StocksData()
# stock.symbol = "AAPL"
# stock.ask = 123.45
# stock.date = datetime.datetime.now()
#
# df = pd.DataFrame(columns=["symbol","date"])
#
# #print(stock.to_pandas())
# df.set_index(["symbol", "date"], inplace=True)
#
# ds = stock.to_pandas_df()
# df = df.append(ds)
# stock.symbol = "BA"
# stock.ask = 37.45
# stock.date = datetime.datetime.now()
# ds = stock.to_pandas_df()
# df = df.append(ds)
#
# dict1 = {}
# for symbol, time in df.index.values:
#     print(symbol)
#     print(df.loc[[,stock.date]][["ask","bid"]])

#print(dict1)
#df = df.append(ds)

#print(df.tail())
# stocks = imp_yahoo.import_data(stock_symbol=["C", "BA", "T"], from_date="2000-01-01", to_date="2017-02-16", reload_data=False,
#                                reload_sp500_symbols=False)
#
# stocks.set_index(["symbol", "date"], inplace=True)
# stocks.sort_index(inplace=True)
# #stocks = stocks.swaplevel("symbol", "date")
# print(stocks.loc[["BA", "T"]])
#print(stocks.iloc[-5:-1])

# dict1 = [{
#         "val1": "A",
#         "val2": "1",
#         "val3": "2.3"
# }]
#
# df = pd.DataFrame(columns=dict1[0].keys())
# df = df.append(dict1)
#df.loc[len(df)]=["1"]
#print(df)


import quantipy.data_management.data_handler as qd
import queue

events = queue.Queue()
dict1 = {}
yahoo = qd.YahooHistoricalHandler(events, ["BA", "T"])


yahoo.stream_data()
yahoo.stream_data()
yahoo.stream_data()
yahoo.stream_data()


# for stock in stocks:
#     print(stock)



# strategy = ["ABC"]
# system_x  = ["Stocksystem"]
# system_x_params = (1,2,3)
#
#
# for strat in strategy:
#     for system in system_x:
#         strategy.execute(system)



# style.use('ggplot')
#
# # start = dt.datetime(2000, 1, 1)
# # end = dt.datetime(2016, 12, 31)
# #
# # df = web.DataReader('TSLA', 'yahoo', start, end)
# # df.to_csv('./Data/tsla.csv')
#
# df = pd.read_csv('./Data/tsla.csv', parse_dates=True, index_col=0)
# #Insert and calculate 100ma
# #df['100ma'] = df['Adj Close'].rolling(window=100,min_periods=0).mean()
# #Drop all values that have NaN included
# #df.dropna(inplace=True)
#
# df_ohlc = df['Adj Close'].resample('1W').ohlc()
# df_volume = df['Volume'].resample('1W').sum()
#
# df_ohlc.reset_index(inplace=True)
# df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
#
# print(df_ohlc.head())
#
# #df['Adj Close'].plot()
# #plt.show()
#
# ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
# ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
# ax1.xaxis_date()
#
# candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
# ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
#
# #ax1.plot(df.index, df['Adj Close'])
# #ax1.plot(df.index, df['100ma'])
#
#
# plt.show()