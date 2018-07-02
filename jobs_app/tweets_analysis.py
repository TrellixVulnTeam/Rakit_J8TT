import pandas as pd
import pymongo
from pymongo import MongoClient
from collections import Counter
import platform
from datetime import timedelta, date
from pylab import *
import sys
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
    df_list.rename(index=str, columns={"index": "dates", 0: occurrence}, inplace=True)
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
    df_null = create_df(cursor_null,'null_occurrence', '2016-01')
    df_final = pd.merge_ordered(df_bearish, df_bullish)
    df_final = pd.merge_ordered(df_final, df_null)
    df_final.fillna('0', inplace=True)
    df_final = df_final.to_html()
    df_final = df_final.replace('<table border="1" class="dataframe">','<table id="twitter_table" class="table table-striped table-bordered table-hover" cellspacing="0" width="100%">')
    return df_final

# Do a daily analysis of bullish vs bearish
#
# def adj_close_vs_tweets(stock,start,end):
#     listed_site = 'yahoo'
#     client = MongoClient('localhost', 27017)
#     db = client['Twitter_data']
#     db_cm = db[stock]
#     cursor_bullish = db_cm.find({'sentiments': 'Bullish'}).sort('created_at', pymongo.DESCENDING)
#     cursor_bearish = db_cm.find({'sentiments': 'Bearish'}).sort('created_at', pymongo.DESCENDING)
#     df_bearish = create_df(cursor_bearish, 'bearish_occurrence', '2018-03', '%Y-%m-%d')
#     df_bullish = create_df(cursor_bullish, 'bullish_occurrence', '2018-03', '%Y-%m-%d')
#     df_final = pd.merge_ordered(df_bearish, df_bullish)
#     df_final.fillna('0', inplace=True)
#     table = stk.get_data(listed_site, start, end)
#     # print(table)
#     # sys.exit()
#     table = table['Adj Close']
#     print(table)
#     # sys.exit()
#     df_final = pd.merge_ordered(df_final, table.to_frame())
# 
#     print(df_final)
#
#
# stock = 'SNE'
#
# stk = Yahoo_finance.Stock(stock)
# listed_site = 'yahoo'
# today = date.today()
# end = date.today()
# start = today - timedelta(30)
#
# # print(table['Adj Close'])
#
# adj_close_vs_tweets(stock,start,end)

# table = create_twitter_data_table(stock_symbol)