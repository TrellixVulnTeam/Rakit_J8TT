from django.shortcuts import render
from django.views.generic import TemplateView
import sys
import platform
import datetime as dt
from datetime import timedelta, date
from django.shortcuts import render
from django.http import HttpResponse
from pylab import *
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient

env = (platform.system())
if env == 'Windows':
    sys.path.insert(0, r".\jobs_app")
elif env == 'Darwin':
    sys.path.insert(0, r"/Users/kamalqureshi/Desktop/Work/Rakit/jobs_app")
else:
    sys.path.insert(0, r"/home/ubuntu/jobs_site/jobs_app")
import Yahoo_finance

# Create your views here.

def index(request):
    return render(request, 'jobs_app/index.html')

def error_404(request):
    data = {}
    return render(request, 'jobs_app/404.html', data)

class Stock_Page(TemplateView):

    def submit(request):

        if '1w' in request.POST:
            today = date.today()
            yesterday = today - timedelta(7)
            start = yesterday
            end = today

        elif '1m' in request.POST:
            today = date.today()
            yesterday = today - timedelta(30)
            start = yesterday
            end = today

        elif '3m' in request.POST:
            today = date.today()
            yesterday = today - timedelta(90)
            start = yesterday
            end = today

        elif '6m' in request.POST:
            today = date.today()
            yesterday = today - timedelta(180)
            start = yesterday
            end = today

        elif '1y' in request.POST:
            today = date.today()
            yesterday = today - timedelta(365)
            start = yesterday
            end = today

        elif 'max' in request.POST:
            today = date.today()
            yesterday = today - timedelta(10000)
            start = yesterday
            end = today

        else:
            today = request.POST.get('dp6', '')
            yesterday = request.POST.get('dp7', '')
            today = today.split(' ')[0]
            yesterday = yesterday.split(' ')[0]
            start = yesterday
            end = today

        info = request.POST.get('info_name', '')
        stock = info
        stk = Yahoo_finance.Stock(stock)
        listed_site = 'yahoo'


        # close_val = str(stk.yesterday_closing_val(listed_site))
        # close_val = close_val.replace('[', '')
        # close_val = close_val.replace(']', '')
        # print(close_val)

        table = stk.get_data(listed_site,start,end)

        # only display Table and Graph if dataframe is valid (i.e has values)
        if str(type(table)) != "<class 'str'>":
            table2 = table.to_html(table_id='exmaple', classes='table table-striped table-bordered table-hover')
            table2 = table2.replace(
                '<table border="1" class="dataframe table table-striped table-bordered table-hover" id="exmaple">',
                '<table id="example" class="table table-striped table-bordered table-hover" cellspacing="0" width="100%">')
            table2 = table2.replace("""      <th></th>
      <th>Open</th>
      <th>High</th>
      <th>Low</th>
      <th>Close</th>
      <th>Adj Close</th>
      <th>Volume</th>""","""      <th>Date</th>
      <th>Open</th>
      <th>High</th>
      <th>Low</th>
      <th>Close</th>
      <th>Adj Close</th>
      <th>Volume</th>""")
            table2 = table2.replace("""    <tr>
      <th>Date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>""","")
            data = table['Adj Close']

            rm = stk.get_rolling_mean(data, 20)
            rstd = stk.get_rolling_std(data, 20)
            upper_band, lower_band = stk.get_bollinger_bands(rm, rstd)
            data.plot(label=stock)
            rm.plot(label='Rolling mean')
            upper_band.plot(label='upper band')
            lower_band.plot(label='lower band')
            plt.title('Bollinger Bands')
            plt.legend(loc='best')
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.grid(True)
            plt.savefig('/Users/kamalqureshi/Desktop/Work/Rakit/jobs_app/static/images/Bands.png', format='png')
            plt.close()

            # For Earnings
            client = MongoClient('localhost', 27017)
            db = client['ZACKS']
            collection_name = 'ZACKS_earnings'
            db_cm = db[collection_name]
            Earnings = db_cm.find({'Symbol': stock})

            # Convert Dictionary to dataframe and then convert to html table
            list_earnings = []

            for post in Earnings:
                list_earnings.append(post)

            df_earnings = pd.DataFrame(list_earnings)
            df_earnings = df_earnings.to_html()
            df_earnings = df_earnings.replace('<table border="1" class="dataframe">','<table id="df_earnings" class="table table-striped table-bordered table-hover" cellspacing="0" width="100%">')

            # For Dividends
            collection_name = 'ZACKS_dividends'
            db_cm = db[collection_name]
            Dividends = db_cm.find({'Symbol': stock})

            list_dividends = []

            for post2 in Dividends:
                list_dividends.append(post2)

            # Convert Dictionary to dataframe and then convert to html table
            df_dividends = pd.DataFrame(list_dividends)
            df_dividends = df_dividends.to_html()
            df_dividends = df_dividends.replace('<table border="1" class="dataframe">','<table id="df_dividends" class="table table-striped table-bordered table-hover" cellspacing="0" width="100%">')


        return render(request, 'jobs_app/index.html', {'table': table2, 'Earnings': df_earnings, 'Dividends': df_dividends})
