import pandas as pd
import numpy as np
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
from datetime import timedelta, date
import datetime as dt
import matplotlib.pyplot as plt

# comment/uncomment mass code is ctrl + /

class Stock:

    def __init__(self,stock_name):
        self.name = stock_name

    def get_data(self,listed_site,start,end):
        self.data = None
        temp = 1
        while self.data is None:
            try:
                print("inside try", temp)
                self.data = web.DataReader(self.name, listed_site, start, end)
                self.data = self.data.round(2)
                self.data.fillna(method="ffil", inplace="TRUE")
                self.data.fillna(method="bfil", inplace="TRUE")
            except:
                temp = temp + 1
                if temp >= 5:
                    self.data = pd.DataFrame()
                pass
        if self.data.empty:
            self.data='unable to fetch data, please check symbol: ' + self.name
        return self.data

    # this one should be like the one from udacity where you pass a list of symbols
    def get_multiple_data(self):
        pass

    def yesterday_closing_val(self,listed_site):
        start = (date.today() - timedelta(1))
        end = start
        df = Stock.get_data(self,listed_site,start,end)

        if str(type(df)) != "<class 'str'>":
            self.closing=(df['Close'].values)
        else:
            self.closing = df
        return self.closing

    def get_rolling_mean(self,values,window):
        self.rolling_mean = values.rolling(window).mean()
        return self.rolling_mean

    def get_rolling_std(self,values,window):
        self.rolling_std = values.rolling(window).std()
        return self.rolling_std

    def get_bollinger_bands(self,rm, rstd):
        self.upper_band = rm + rstd * 2
        self.lower_band = rm - rstd / 2
        return self.upper_band,self.lower_band

    def compute_daily_returns(self, df):
        self.daily_returns = df.copy()
        self.daily_returns[1:] = (df[1:] / df[:-1].values) -1
        self.daily_returns.ix[0] = 0
        return self.daily_returns




    # Create a def for getting 1 month data, 1 week, 1 day, 3 months, 6 months, 1 year, all

#
#
# stock_name = 'AAPL'
# listed_site = 'yahoo'
# start = dt.datetime(2018, 1, 1)
# end = dt.datetime(2018, 3, 1)
# stk = Stock(stock_name)
# data = stk.get_data(listed_site,start,end)
# print(data)
# data = data['Adj Close']
# print(data)

# rm = stk.get_rolling_mean(data,20)
# rstd = stk.get_rolling_std(data,20)
# upper_band, lower_band = stk.get_bollinger_bands(rm, rstd)
# ax = data.plot(title="Bollinger Bands", label=stock_name)
# rm.plot(label='Rolling mean', ax=ax)
# upper_band.plot(label='upper band', ax=ax)
# lower_band.plot(label='lower band', ax=ax)
# ax.set_xlabel("Date")
# ax.set_ylabel("Price")
# ax.legend(loc='upper left')
# plt.show()

# daily_returns = stk.compute_daily_returns(data)
#ax = daily_returns.plot(title="Daily returns", label=stock_name)
# ax.set_xlabel("Date")
# ax.set_ylabel("Price")
# ax.legend(loc='upper left')

#plt.show()

# make this histogram plotting, getting means and std as a def in the class

#Plot a histogram
#daily_returns.hist()
# daily_returns.hist(bins=20) # changing # of bins to 20
#
# mean = daily_returns.mean()
# std = daily_returns.std()
# # print(mean)
#
# plt.axvline(mean,color='w',linestyle='dashed',linewidth=2)
# plt.axvline(std,color='r',linestyle='dashed',linewidth=2)
# plt.axvline(-std,color='r',linestyle='dashed',linewidth=2)

#compute kurtosis
# print(daily_returns.kurtosis())


# #Scatter plot AAPL vs SPY
# daily_returns.plot(kind='scatter', x='SPY', y='XOM')
# beta_XOM,alpha_XOM = np.polyfit(daily_returns['SPY'],daily_returns['XOM'],1)
# plt.plot(daily_returns['SPY'], beta_XOM*daily_returns['SPY']+alpha_XOM, '-', color='r')
# plt.show()
#
# #Calculate the correlation coefficient
# print(daily_returns.corr(method='pearson'))

#print(rm)

#Todo- Make the get_data funciton more like the one from udacity, where you pass a list of symbols
#Todo- Make each one of the plots a function, possibly have a compare to SPY fucntion to compare our data vs SPY data


# data = stk.yesterday_closing_val(listed_site)
#print (data)