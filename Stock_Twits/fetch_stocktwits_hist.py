import json, sys
import requests
import pandas as pd
import time
import datetime as dt
pd.set_option('display.width',1000)

starttime = dt.datetime.now()

API_URL = r'https://api.stocktwits.com/api/2/'
THROTTLE_REQ_MIN = 180 #sec

def fetch_stock_stream_from_stocktwits(symbol, max_id = None):
    print('Fetching data...')
    try:
        if max_id == None:
            resp = requests.get(API_URL + 'streams/symbol/{}.json'.format(symbol))
            print('Time stamp : ' , dt.datetime.now(), '---> In If statement line # 19 Using Id:', max_id)
        else:
            print('Time stamp : ', dt.datetime.now(), '---> In else statement line # 21 Using Id:', max_id)
            temp = None
            counter =0

            while temp is None:
                try:
                    resp = requests.get(API_URL + 'streams/symbol/{}.json'.format(symbol), params={'max': '{}'.format(max_id)})
                    df = pd.DataFrame(json.loads(resp.text).get('messages', ''))
                    last_record = df.iloc[-1]
                    print('Time stamp : ', dt.datetime.now(), '--->  last record is: ', last_record['id'])
                    df.to_pickle('./hist/{}_{}_{}.p'.format(symbol, last_record['created_at'][0:19].replace(':', '-'),last_record['id']))
                    print(df)
                    temp = df
                    return last_record['id']
                except:
                    counter = counter + 1
                    print('Time stamp : ', dt.datetime.now(), '--->  Error fetching data counter = ', counter)
                    time.sleep(THROTTLE_REQ_MIN)
                    if counter >= 3:
                        print('Time stamp : ', dt.datetime.now(), '--->  Counter failed to many times... counter = ', counter)
                        print('Time stamp : ', dt.datetime.now(), '--->  Could not get data.. exiting scrpit')
                        sys.exit()
                    pass

        df = pd.DataFrame(json.loads(resp.text).get('messages', ''))
        last_record = df.iloc[-1]
        print('Time stamp : ', dt.datetime.now(), '--->  last record is: ', last_record['id'])
        df.to_pickle('./hist/{}_{}_{}.p'.format(symbol, last_record['created_at'][0:19].replace(':', '-'),
                                                last_record['id']))
        print(df)
        temp = df
        return last_record['id']

        #TODO: expand this to be able to fetch using burst, and cycle throught multiple tokens
        # print(resp.headers)
        # print(resp.headers.get('X-RateLimit-Limit',''))
        # print(resp.headers.get('X-RateLimit-Remaining',''))
        # print(dt.datetime.fromtimestamp(int(resp.headers.get('X-RateLimit-Reset',0))))

    except:
        print('Exception throw, verify the last id that was saved for instrument {}'.format(symbol))

    print('Current elapsed time:', dt.datetime.now() - starttime)

if len(sys.argv) == 2:
    print('Time stamp : ', dt.datetime.now(), '--->  Starting fresh for symbol:',sys.argv[1])

    max_id = fetch_stock_stream_from_stocktwits(sys.argv[1])

    print('Time stamp : ', dt.datetime.now(), ' ---> max id', max_id)
    while True:
        time.sleep(THROTTLE_REQ_MIN)
        max_id = fetch_stock_stream_from_stocktwits(sys.argv[1],max_id)


elif len(sys.argv) == 3:
    print('Time stamp : ', dt.datetime.now(), '--->  Starting where we last left off for symbol {} with id older than {}'.format(sys.argv[1],sys.argv[2]))
    count = 0
    while True:
        time.sleep(THROTTLE_REQ_MIN)
        if count == 0:
            max_id = fetch_stock_stream_from_stocktwits(sys.argv[1],sys.argv[2])
            print('Time stamp : ', dt.datetime.now(), '--->  Inside if line #83 max id', max_id)
            count = count + 1
        else:
            max_id = fetch_stock_stream_from_stocktwits(sys.argv[1], max_id)
            print('Time stamp : ', dt.datetime.now(), '--->  Inside else line # 87 max id', max_id)

else:
    print('Invalid argument was provided')
    sys.exit()
