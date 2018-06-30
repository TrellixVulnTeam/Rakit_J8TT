import pandas as pd
import numpy as np
import os
import datetime as dt
from collections import defaultdict
pd.set_option('display.width',1000)
import pymongo
import json
import sys

key_symbol = 'DIS'

symbol_dict = defaultdict(list)
for root, dirs, files in os.walk('/Users/kamalqureshi/Desktop/Work/Rakit/Twitter_Data/' + key_symbol):
    for f in files:
        if '.p' in f:
            symbol = f.split('_')[0]
            symbol_dict[symbol].append('/Users/kamalqureshi/Desktop/Work/Rakit/Twitter_Data/' + key_symbol + '/{}'.format(f))
    print('Finished putting symbol_dict list')


def get_list_of_repeating_keys(element, dict_key):
    urls = []
    try:
        for x in element:
            urls.append(x.get(dict_key, np.nan) if type(x) is dict else np.nan)
    except:
        urls
    finally:
        return urls


def write_to_db(df,db_name,collection_name):
    mng_client = pymongo.MongoClient('localhost', 27017)
    mng_db = mng_client[db_name]
    db_cm = mng_db[collection_name]

    df_json = json.loads(df.T.to_json()).values()

    for x in df_json:
        print(x)
        db_cm.insert(x)

    print('Finished Updating', collection_name)


list_data = []
df = pd.DataFrame

for key, value in symbol_dict.items():
    print('Combined data for', key,'\n')
    for x in value:
        temp_data = pd.read_pickle(x)
        list_data.append(temp_data)
    df = pd.concat(list_data)
    df.reset_index(inplace=True)
    # df.set_index('id',inplace=True)
    df['created_at'] = df['created_at'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ'))
    df['sentiments'] = df['entities'].apply(lambda x: x.get('sentiment', np.nan).get('basic',np.nan) if x.get('sentiment', np.nan) != None else np.nan)
    df['username'] = df['user'].apply(lambda x: x.get('username', np.nan))
    df['followers'] = df['user'].apply(lambda x: x.get('followers',np.nan))
    df['urls'] = df['links'].apply(lambda x: get_list_of_repeating_keys(x, 'url'))
    df['symbols'] = df['symbols'].apply(lambda x: get_list_of_repeating_keys(x, 'symbol'))
    df.drop(['user','conversation','entities','likes','mentioned_users','reshare_message','source','index','reshares','links'], axis=1, inplace= True)


    df.to_pickle('/Users/kamalqureshi/Desktop/Work/Rakit/Twitter_Data/' + key_symbol + '_master_data.p')
    print(df)
    collection_name = key_symbol
    write_to_db(df,'Twitter_data',collection_name)