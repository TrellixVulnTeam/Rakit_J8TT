from django.views.generic import TemplateView
import sys
import platform
from datetime import timedelta, date
from django.shortcuts import render
from pylab import *

env = (platform.system())
if env == 'Windows':
    sys.path.insert(0, r".\jobs_app")
elif env == 'Darwin':
    sys.path.insert(0, r"/Users/kamalqureshi/Desktop/Work/Rakit/jobs_app")
else:
    sys.path.insert(0, r"/home/ubuntu/jobs_site/jobs_app")
import Yahoo_finance
import tweets_analysis
import zacks_analysis
import graph_analysis

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

        table = stk.get_data(listed_site,start,end)

        # only display table, graph, zacks, and twitter data if dataframe is valid (i.e has values)
        if str(type(table)) != "<class 'str'>":

            table_data = graph_analysis.create_data_table(table)
            graph_analysis.create_bollinger_graph(stock, table)

            df_earnings = zacks_analysis.create_zacks_df(stock, 'ZACKS_earnings', 'df_earnings')
            df_dividends = zacks_analysis.create_zacks_df(stock,'ZACKS_dividends', 'df_dividends')

            twitter_table = tweets_analysis.create_twitter_data_table(stock)

            return render(request, 'jobs_app/index.html',
                          {'table': table_data, 'Earnings': df_earnings, 'Dividends': df_dividends,
                           'twitter_table': twitter_table})

        return render(request, 'jobs_app/index.html')
