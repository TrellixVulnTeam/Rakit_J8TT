import unittest
import sys
import datetime as dt
from datetime import timedelta, date
sys.path.insert(0, r"..\personal")
import Yahoo_finance

class Test(unittest.TestCase):

    def test_get_data(self):
        stock_name = 'TSLA'
        listed_site = 'yahoo'
        start = dt.datetime(2018, 1, 1)
        end = dt.datetime(2018, 1, 2)
        stk = Yahoo_finance.Stock(stock_name)
        data = stk.get_data(listed_site,start,end)
        close_val = int(data['Close'].values)
        self.assertEqual(close_val,320)

if __name__ == '__main__':
    unittest.main()