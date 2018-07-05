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


pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


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


def fetch_zack(symbol, zack_type, start):
    client = MongoClient('localhost', 27017)
    db = client['ZACKS']
    db_cm = db[zack_type]
    data = db_cm.find({'Symbol': symbol}).sort('created_at', pymongo.DESCENDING)

    list_zacks = []

    for x in data:
        # print(x['Datetime'])
        create_date = datetime.datetime.fromtimestamp(x['Datetime']/ 1000).strftime('%Y-%m-%d')
        # print(create_date)
        if create_date >= start:
            list_zacks.append(x)
            # print('true',x)
    df = pd.DataFrame(list_zacks)
    #print(data)
    return df



def price_vs_tweets(stock,start,end):
    listed_site = 'yahoo'
    client = MongoClient('localhost', 27017)
    db = client['Twitter_data']
    db_cm = db[stock]
    cursor_bullish = db_cm.find({'sentiments': 'Bullish'}).sort('created_at', pymongo.DESCENDING)
    cursor_bearish = db_cm.find({'sentiments': 'Bearish'}).sort('created_at', pymongo.DESCENDING)
    df_bearish = create_df(cursor_bearish, 'bearish_occurrence', '2016-01', '%Y-%m-%d')
    df_bullish = create_df(cursor_bullish, 'bullish_occurrence', '2016-01', '%Y-%m-%d')
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

    # print(df_final)
    # print(list(df_final))

    return df_final

    #THIS WORKSS
    # df_final = df_final.astype(float)
    #
    #
    # fig, ax1 = plt.subplots()
    # #
    # ax1.plot(df_final.bearish_occurrence, color='red')
    # ax1.plot(df_final.bullish_occurrence, color='blue')
    # ax2 = ax1.twinx()
    # ax2.plot(df_final.Adj_Close, color='green')
    # ax1.legend(loc=2)
    # ax2.legend(loc=1)
    #
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

#     print(df_final)
#     print(list(df_final))
#


#THIS WORKS TOO
# stock = 'JPM'
#
# stk = Yahoo_finance.Stock(stock)
# listed_site = 'yahoo'
# today = date.today()
# end = date.today()
# start = today - timedelta(800)
#
# # price_vs_tweets(stock,start,end)
#
# tweets_price = price_vs_tweets(stock,start,end)
# tweets_price.index = pd.to_datetime(tweets_price.index)
# print(tweets_price)
# print('\nnext')
#
#
# # print(tweets_price)
#
# #fetch_zack(stock,'ZACKS_dividends','2018-01-01')
# # print(fetch_zack(stock,'ZACKS_dividends','2018-01-01'))
# temp_zacks = fetch_zack(stock,'ZACKS_earnings','2016-01-01')
# # print(temp_zacks)
# # print('AFTER')
# #print(list(temp_zacks))
# #temp_zacks = temp_zacks['Datetime','Company', 'Estimate','Reported']
# temp_zacks = temp_zacks.drop([ 'Company','ESP',  'Key', 'Mrk_Cap(M)', 'Price_Change', 'Report', 'Symbol', 'Time', 'Type', '_id'], axis=1)
#
# #temp_zacks['Datetime'] = datetime.datetime.fromtimestamp(temp_zacks['Datetime'] / 1000).strftime('%Y-%m-%d')
# temp_zacks['Datetime'] = pd.to_datetime(temp_zacks['Datetime'], unit='ms')
#
# temp_zacks.rename(index=str, columns={'Datetime': 'Date'}, inplace=True)
# temp_zacks.set_index('Date', inplace=True)
# temp_zacks.replace('--', NaN , inplace=True)
# print(temp_zacks)
# print('\nnext')
#
# #zacks_tweets_price = pd.merge(tweets_price, temp_zacks, how='inner', left_index=True, right_index=True)
# #zacks_tweets_price = pd.concat(tweets_price, temp_zacks)
# zacks_tweets_price = pd.concat([tweets_price, temp_zacks], axis=0, sort=True)
#
# zacks_tweets_price.sort_index(axis=0, inplace=True)
# zacks_tweets_price.index = pd.to_datetime(zacks_tweets_price.index)
# zacks_tweets_price.index = zacks_tweets_price.index.strftime('%Y-%m-%d')
# print(zacks_tweets_price)
# print(list(zacks_tweets_price))
#
#
# zacks_tweets_price = zacks_tweets_price.astype(float)
# #
# #
# fig, ax1 = plt.subplots()
# #
# ax1.plot(zacks_tweets_price.bearish_occurrence, color='red')
# ax1.plot(zacks_tweets_price.bullish_occurrence, color='blue')
#
# ax2 = ax1.twinx()
# ax2.plot(zacks_tweets_price.Adj_Close, color='green')
#
#
# coord_x1 = 0.5
# coord_y1 = 5
#
# coord_x2 = 100
# coord_y2 = 25
#
# x = 20
# y = 25
#
# # plt.plot([coord_x1, coord_x2], [coord_y1, coord_y1], '-o')
# # plt.plot('2018-02-03', y, '-o', label='earning')
# #
# # plt.axvline(5, color='g', linestyle='--')
#
# plt.plot(zacks_tweets_price.Estimate,  '-o')
# plt.plot(zacks_tweets_price.Reported,  '-o')
#
# # ax2.plot(zacks_tweets_price.Estimate, color='black', '-o')
# # ax2.plot(zacks_tweets_price.Reported, color='black', '-o')
# # ax3 = ax1.twinx()
# ax1.legend(loc=2)
# ax2.legend(loc=1)
#
# # y=[2.56422, 3.77284,3.52623,3.51468,3.02199]
# # z=[0.15, 0.3, 0.45, 0.6, 0.75]
# # n=[58,651,393,203,123]
# #
# # fig, ax = plt.subplots()
# # ax.scatter(z, y)
# #
# # for i, txt in enumerate(n):
# #     ax.annotate(txt, (z[i],y[i]))
# plt.show()
#
# # table = create_twitter_data_table(stock_symbol)