import pandas as pd
import pymongo
from pymongo import MongoClient
import datetime
from collections import Counter

def create_twitter_data_table(stock_symbol):
    client = MongoClient('localhost', 27017)
    db = client['Twitter_data']
    db_cm = db[stock_symbol]
    cursor_bullish = db_cm.find({'sentiments': 'Bullish'}).sort('created_at', pymongo.DESCENDING)
    cursor_bearish = db_cm.find({'sentiments': 'Bearish'}).sort('created_at', pymongo.DESCENDING)
    cursor_null = db_cm.find({'sentiments': None}).sort('created_at', pymongo.DESCENDING)


    def create_df (cursor,occurrence):
        list_summary = []
        for data in cursor:
            create_date_epoch = data['created_at']
            create_month = datetime.datetime.fromtimestamp(create_date_epoch / 1000).strftime('%Y-%m')
            if (create_month >= '2016-01'):
                list_summary.append(create_month)
        list_summary = Counter(list_summary)
        df_list= pd.DataFrame.from_dict(list_summary, orient='index').reset_index()
        df_list.rename(index=str, columns={"index": "dates", 0: occurrence}, inplace=True)
        return df_list


    df_bearish = create_df(cursor_bearish,'bearish_occurrence')
    df_bullish = create_df(cursor_bullish,'bullish_occurrence')
    df_null = create_df(cursor_null,'null_occurrence')
    df_final = pd.merge_ordered(df_bearish, df_bullish)
    df_final = pd.merge_ordered(df_final, df_null)
    df_final.fillna('0', inplace=True)
    df_final = df_final.to_html()
    df_final = df_final.replace('<table border="1" class="dataframe">','<table id="twitter_table" class="table table-striped table-bordered table-hover" cellspacing="0" width="100%">')
    return df_final