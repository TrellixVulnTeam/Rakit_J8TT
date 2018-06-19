from django.shortcuts import render
import sys
import platform
import datetime as dt
from datetime import timedelta, date
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

    elif 'ytd' in request.POST:
        today = date.today()
        yesterday = today - timedelta(10000)
        start = yesterday
        end = today

    else:
        today = date.today()
        yesterday = today - timedelta(1)
        start = yesterday
        end = today



    info = request.POST.get('info_name', '')
    stock = info
    stk = Yahoo_finance.Stock(stock)
    listed_site = 'yahoo'
    close_val = str(stk.yesterday_closing_val(listed_site))
    close_val = close_val.replace('[', '')
    close_val = close_val.replace(']', '')
    print(close_val)


    table = stk.get_data(listed_site,start,end)
    if str(type(table)) != "<class 'str'>":
        table = table.to_html(table_id='exmaple', classes='table table-striped table-bordered table-hover')
        table = table.replace(
            '<table border="1" class="dataframe table table-striped table-bordered table-hover" id="exmaple">',
            '<table id="example" class="table table-striped table-bordered table-hover" cellspacing="0" width="100%">')
        table = table.replace('<th></th>', '<th>Date</th>')
        table = table.replace("""<tr>
      <th>Date</th>
      <th>Date</th>
      <th>Date</th>
      <th>Date</th>
      <th>Date</th>
      <th>Date</th>
      <th>Date</th>
    </tr>""", '')

    return render(request, 'jobs_app/index.html', {'name':stock, 'close_val':close_val, 'listed_site':listed_site, 'table': table})
