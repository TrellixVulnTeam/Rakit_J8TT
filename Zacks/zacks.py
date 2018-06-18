import requests, json
import pandas as pd
import datetime as dt
import warnings
import sys
warnings.filterwarnings('ignore')
pd.set_option('display.width', 1000)

stop_at_historical = dt.datetime(2018,6,12)  #I am seeing 'Symbol' being printed on exception/console...investiage
stop_at_historical = (dt.datetime.now() - stop_at_historical).days

list_earnings = []
list_dividends = []
def get_earnings(date):
    try:
        epoch_date = int((date - dt.datetime(1970, 1, 1)).total_seconds())
        print(' - Date Time:', date, '| Epoch Time:', epoch_date)
        req = requests.get(
            'https://www.zacks.com/includes/classes/z2_class_calendarfunctions_data.php?calltype=eventscal&date={}&type=1'.format(
                epoch_date))
        data = json.loads(req.text)
        empty_data_len = len(str(data))
        if empty_data_len != 12:
            df = pd.DataFrame(data['data'])
            df['Datetime'] = date
            df['Type'] = 'Earnings'
            list_earnings.append(df)
            df.rename_axis(
                {0: 'Symbol', 1: 'Company', 2: 'Mrk_Cap(M)', 3: 'Time', 4: 'Estimate', 5: 'Reported', 6: 'ESP',
                 7: 'Price_Change',
                 8: 'Report', 9: 'Blank'}, axis='columns', inplace=True)

            if 'Blank' in list(df):
                df.drop('Blank', axis=1, inplace=True)

            df['Symbol'] = df['Symbol'].str.extract(r'rel="(.+?)" class', expand=True)
            df['Company'] = df['Company'].str.extract(r'>(.+?)<', expand=True)
            df['ESP'] = df['ESP'].str.extract(r'>(.+?)<', expand=True)
            df['Price_Change'] = df['Price_Change'].str.extract(r'>(.+?)<', expand=True)
            df['Report'] = df['Report'].str.extract(r'>(.+?)<', expand=True)
            df['ESP'] = df['ESP'].str.strip()
            df['Price_Change'] = df['Price_Change'].str.strip()
            df.to_pickle('./output/{}_zacks_earning'.format(date.strftime('%Y_%m_%d')))
    except Exception as e:
        print(e)


def get_dividends(date):
    try:
        epoch_date = int((date - dt.datetime(1970, 1, 1)).total_seconds())
        req = requests.get(
            'https://www.zacks.com/includes/classes/z2_class_calendarfunctions_data.php?calltype=eventscal&date={}&type=5'.format(
                epoch_date))
        data = json.loads(req.text)
        empty_data_len = len(str(data))
        if empty_data_len != 12:
            df = pd.DataFrame(data['data'])
            df['Datetime'] = date
            df['Type'] = 'Dividends'
            # print(df)
            list_dividends.append(df)

            df.rename_axis(
                {0: 'Symbol', 1: 'Company', 2: 'Mrk_Cap(M)', 3: 'Amount', 4: 'Yield', 5: 'Ex-Div Date', 6: 'Current_Price',
                 7: 'Payable_Date'}, axis='columns', inplace=True)
            try:
                df['Symbol'] = df['Symbol'].str.extract(r'rel="(.+?)" class', expand=True)
            except:
                pass
            df['Company'] = df['Company'].str.extract(r'>(.+?)<', expand=True)
            df.to_pickle('./output/{}_zacks_dividends'.format(date.strftime('%Y_%m_%d')))
    except Exception as e:
        print(e)

current_date = dt.datetime.now().replace(hour=5, minute=0, second=0, microsecond=0)
epoch_current_date = int((current_date - dt.datetime(1970, 1, 1)).total_seconds())
print(current_date, epoch_current_date)
date_list = [current_date - dt.timedelta(days=x) for x in range(0, stop_at_historical)]
# print(date_list)

print('Fetching Earning and Dividend releases for:')
for date in reversed(date_list):
    get_earnings(date)
    get_dividends(date)

#Consolidate into a single dataset
df_earnings = pd.concat(list_earnings)
df_dividends = pd.concat(list_dividends)

print('\n\nEarnings\n', df_earnings.head(15))
print('\nDividends\n', df_dividends.head(15))


zacks_filestring = '{}'.format(dt.datetime.today().strftime("%m_%d_%Y"))

zacks_endtime = dt.datetime.now()