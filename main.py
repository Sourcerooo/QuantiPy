#ds.convert_optionvue_csv("./Data/OptionVue/20150105.csv")

import quantipy.basics.data as qdata

import quantipy.data_management.data_import as conv

import pandas as pd



#imp_ov = conv.OptionVueImport()
#stock_data, future_date, option_date = imp_ov.import_data(filename="./Data/OptionVue/20150106.csv")
#print(option_date)

# stocks, futures, options = imp_ov.import_csv("./Data/OptionVue/20150106.csv")
#
# for stock in stocks:
#     print(stock)

import quantipy.data_management.data_import as di
imp_yahoo = di.YahooStockImport()

stocks = imp_yahoo.import_data(stock_symbol=["T"], from_date="1970-01-01", to_date="2017-02-16", reload_data=False,
                               reload_sp500_symbols=False)

print(stocks.head())
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