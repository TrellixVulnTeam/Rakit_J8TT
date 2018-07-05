from pylab import *
import matplotlib.pyplot as plt
import platform

env = (platform.system())
if env == 'Windows':
    sys.path.insert(0, r".\jobs_app")
elif env == 'Darwin':
    sys.path.insert(0, r"/Users/kamalqureshi/Desktop/Work/Rakit/jobs_app")
else:
    sys.path.insert(0, r"/home/ubuntu/jobs_site/jobs_app")
import Yahoo_finance


def create_data_table(table):

    # only generate table if data is valid
    if str(type(table)) != "<class 'str'>":
        table = table.to_html(table_id='data', classes='table table-striped table-bordered table-hover')
        table = table.replace(
            '<table border="1" class="dataframe table table-striped table-bordered table-hover" id="exmaple">',
            '<table id="example" class="table table-striped table-bordered table-hover" cellspacing="0" width="100%">')
        table = table.replace("""<th></th>
      <th>Open</th>
      <th>High</th>
      <th>Low</th>
      <th>Close</th>
      <th>Adj Close</th>
      <th>Volume</th>""", """<th>Date</th>
      <th>Open</th>
      <th>High</th>
      <th>Low</th>
      <th>Close</th>
      <th>Adj Close</th>
      <th>Volume</th>""")
        table = table.replace("""<tr>
      <th>Date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>""",'')
        return table

def create_bollinger_graph(stock, table):
        stk = Yahoo_finance.Stock(stock)

        # only generate graph if data is valid
        if str(type(table)) != "<class 'str'>":
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
            plt.savefig('/Users/kamalqureshi/Desktop/Work/Rakit/jobs_app/static/images/Bands.jpg', format='png')
            plt.close()