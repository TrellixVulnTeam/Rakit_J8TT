import pandas as pd
import pymongo
from pymongo import MongoClient
from collections import Counter
import platform
from datetime import timedelta, date
import sys
from pylab import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
env = (platform.system())
if env == 'Windows':
    sys.path.insert(0, r".\jobs_app")
elif env == 'Darwin':
    sys.path.insert(0, r"/Users/kamalqureshi/Desktop/Work/Rakit/jobs_app")
else:
    sys.path.insert(0, r"/home/ubuntu/jobs_site/jobs_app")
import Yahoo_finance


def create_df(cursor, occurrence, start_date, filter_type):
    list_summary = []
    for data in cursor:
        create_date_epoch = data['created_at']
        create_month = datetime.datetime.fromtimestamp(create_date_epoch / 1000).strftime(filter_type)
        if (create_month >= start_date):
            list_summary.append(create_month)
    list_summary = Counter(list_summary)
    df_list = pd.DataFrame.from_dict(list_summary, orient='index').reset_index()
    df_list.rename(index=str, columns={"index": "Date", 0: occurrence}, inplace=True)
    return df_list

def create_twitter_data_table(stock_symbol):
    client = MongoClient('localhost', 27017)
    db = client['Twitter_data']
    db_cm = db[stock_symbol]
    cursor_bullish = db_cm.find({'sentiments': 'Bullish'}).sort('created_at', pymongo.DESCENDING)
    cursor_bearish = db_cm.find({'sentiments': 'Bearish'}).sort('created_at', pymongo.DESCENDING)
    cursor_null = db_cm.find({'sentiments': None}).sort('created_at', pymongo.DESCENDING)

    df_bearish = create_df(cursor_bearish,'bearish_occurrence', '2016-01', '%Y-%m')
    df_bullish = create_df(cursor_bullish,'bullish_occurrence', '2016-01', '%Y-%m')
    df_null = create_df(cursor_null,'null_occurrence', '2016-01','%Y-%m')
    df_final = pd.merge_ordered(df_bearish, df_bullish)
    df_final = pd.merge_ordered(df_final, df_null)
    df_final.fillna('0', inplace=True)
    df_final = df_final.to_html()
    df_final = df_final.replace('<table border="1" class="dataframe">','<table id="twitter_table" class="table table-striped table-bordered table-hover" cellspacing="0" width="100%">')
    return df_final

# Do a daily analysis of bullish vs bearish

def price_vs_tweets(stock,start,end):
    listed_site = 'yahoo'
    client = MongoClient('localhost', 27017)
    db = client['Twitter_data']
    db_cm = db[stock]
    cursor_bullish = db_cm.find({'sentiments': 'Bullish'}).sort('created_at', pymongo.DESCENDING)
    cursor_bearish = db_cm.find({'sentiments': 'Bearish'}).sort('created_at', pymongo.DESCENDING)
    df_bearish = create_df(cursor_bearish, 'bearish_occurrence', '2018-01', '%Y-%m-%d')
    df_bullish = create_df(cursor_bullish, 'bullish_occurrence', '2018-01', '%Y-%m-%d')
    df_final = pd.merge_ordered(df_bearish, df_bullish)
    df_final.fillna('0', inplace=True)
    df_final.set_index('Date', inplace=True)
    table = stk.get_data(listed_site, start, end)
    table.reset_index(inplace=True)


    #table['Date'] = table['Date'].strftime('%Y-%m-%d')
    table['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))


    table.set_index('Date', inplace=True)

    #table.rename(index=str, columns={"Adj Close": "Adj_Close"}, inplace=True)
    df_final = pd.merge(table,df_final,how='inner', left_index=True, right_index=True)
    # print(df_final)
    # print(list(df_final))
    df_final = df_final.drop(['Open', 'High', 'Low', 'Close','Volume'], axis=1)
    df_final.reset_index(inplace=True)

    df_final['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))

    df_final.set_index('Date', inplace=True)
    df_final.rename(index=str, columns={"Adj Close": "Adj_Close"}, inplace=True)
    # df_final.index = df_final.index.strftime('%Y-%m-%d')
    # df_final.index.apply(lambda x: x.strftime('%Y-%m-%d'))

    # df_final.index = df_final.index.split[0]

    print(df_final)
    print(list(df_final))

    # df_final.plot()
    # plt.show()


    # ax1 = df_final.bullish_occurrence.plot(grid=True, label='Bearish')
    # plt.show()

    # ax.plt(df_final.Date,df_final.bearish_occurrence)
    #
    # plt.show()
    #


#    df_final = df_final.astype(float)
    # print(df_final.columns)
    df_final = df_final.astype(float)

    # ax1 = df_final.bearish_occurrence.plot(grid=True, label='Bearish')
    # ax2 = df_final.Adj_Close.plot(grid=True, secondary_y=True, label='Adj Close')
    # ax1 = df_final.bullish_occurrence.plot(grid=True, label='Bullish')
    # ax1.legend(loc=2)
    # ax2.legend(loc=1)
    # plt.show()


    # ax1 = df_final.bullish_occurrence.plot(grid=True, label='Bullish')
    # ax2 = df_final.Adj_Close.plot(grid=True, secondary_y=True, label='Adj Close')
    # ax1.legend(loc=2)
    # ax2.legend(loc=1)

    fig, ax1 = plt.subplots()
    #
    ax1.plot(df_final.bearish_occurrence, color='red')
    ax1.plot(df_final.bullish_occurrence, color='blue')
    ax2 = ax1.twinx()
    ax2.plot(df_final.Adj_Close, color='green')
    ax1.legend(loc=2)
    ax2.legend(loc=1)

    plt.show()
    # # ax1.tick_params(axis='y')
    # ax1.legend(loc=2)
    #
    # ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    # ax2.plot(df_final.Adj_Close, color='green')
    # ax2.legend(loc=1)

    # myFmt = mdates.DateFormatter('%Y-%m-%d')
    # ax1.xaxis.set_major_formatter(myFmt)

    # df_final.index = df_final.index.strftime('%d/%m/%Y')


    #ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))


    # plt.gca().xaxis.set_major_formatter(plt.FixedFormatter(df_final.index.to_series().dt.strftime("%Y-%m-%d")))

#    ax1.xaxis.set_major_formatter(plt.FixedFormatter(df_final.index.to_series().dt.strftime('%Y-%m-%d')))

#    ax1.xaxis = mdates.DateFormatter('%Y-%m-%d')

    #ax2.format_xdata = mdates.DateFormatter('%Y-%m-%d')

    #
    # ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    # ax1.xaxis.set_minor_formatter(mdates.DateFormatter("%Y-%m"))
    #
    # ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    # ax2.xaxis.set_minor_formatter(mdates.DateFormatter("%Y-%m"))

    #
    # color = 'tab:blue'
    # ax2.set_ylabel('sin', color=color)  # we already handled the x-label with ax1
    # ax2.plot(t, data2, color=color)
    # ax2.tick_params(axis='y', labelcolor=color)

    # fig.tight_layout()  # otherwise the right y-label is slightly clipped
    # plt.show()

    # df_final.plot()
    # plt.show()



    # for index, row in df_final.iterrows():
    #     if (int(row['bearish_occurrence']) > int(row['bullish_occurrence'])):
    #         df_final['bull_vs_bear'] = 'bearish'
    #     elif (int(row['bearish_occurrence']) < int(row['bullish_occurrence'])):
    #         df_final['bull_vs_bear'] = 'bullish'
    #     else:
    #         df_final['bull_vs_bear'] = 'equal'




    # Compare bullish vs bearish, see which over is bigger and compare with tomorrows price and check if its right
    #df_final['bull_vs_bear'] = df_final['Adj Close'].eq(df_final['Adj Close'].shift())
    # if (df_final['bearish_occurrence'] > df_final['bullish_occurrence']):
    #     df_final['bull_vs_bear'] = 'bearish'
#




#     print(df_final)
#     print(list(df_final))
#
stock = 'SNE'

stk = Yahoo_finance.Stock(stock)
listed_site = 'yahoo'
today = date.today()
end = date.today()
start = today - timedelta(180)

price_vs_tweets(stock,start,end)

# table = create_twitter_data_table(stock_symbol)