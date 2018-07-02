from django.views.generic import TemplateView
import platform
from datetime import timedelta, date
from django.shortcuts import render
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
import tweets_analysis
import zacks_analysis
import graph_analysis


def index(request):
    return render(request, 'jobs_app/index.html')


def error_404(request):
    data = {}
    return render(request, 'jobs_app/404.html', data)


class Stock_Page(TemplateView):

    def submit(request):

        today = date.today()

        if '1w' in request.POST:
            end = date.today()
            start = today - timedelta(7)

        elif '1m' in request.POST:
            end = date.today()
            start = today - timedelta(30)

        elif '3m' in request.POST:
            end = date.today()
            start = today - timedelta(90)

        elif '6m' in request.POST:
            end = date.today()
            start = today - timedelta(180)

        elif '1y' in request.POST:
            end = date.today()
            start = today - timedelta(365)

        elif 'max' in request.POST:
            end = date.today()
            start = today - timedelta(10000)

        else:
            end = request.POST.get('dp6', '')
            end = end.split(' ')[0]
            start = request.POST.get('dp7', '')
            start = start.split(' ')[0]

        stock = request.POST.get('info_name', '')
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