from django.shortcuts import render
import sys
import platform
import datetime as dt
env = (platform.system())
if env == 'Windows':
    sys.path.insert(0, r".\jobs_app")
elif env == 'Darwin':
    sys.path.insert(0, r"/Users/madeleinepollock/Downloads/jobs_site-2/jobs_app")
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

    info = request.POST.get('info_name', '')
    stock = info
    stk = Yahoo_finance.Stock(stock)
    listed_site = 'yahoo'
    close_val = str(stk.yesterday_closing_val(listed_site))
    close_val = close_val.replace('[', '')
    close_val = close_val.replace(']', '')
    print(close_val)

    start = dt.datetime(2018, 1, 15)
    end = dt.datetime(2018, 2, 1)
    table = stk.get_data(listed_site,start,end)
    if str(type(table)) != "<class 'str'>":
        table = table.to_html()

    return render(request, 'jobs_app/index.html', {'name':stock, 'close_val':close_val, 'listed_site':listed_site, 'table': table})

