import unittest
from desafio import *


class MercadosTest(unittest.TestCase):        
    def test_mercado_trades(self):
        m = Mercado('BTC-CLP')
        self.assertTrue(len(m.getTrades())>0)

    def test_mercado_trades_prices(self):
        m = Mercado('BTC-CLP')
        trade_prices = m.getTradePrices()
        self.assertTrue(len(trade_prices)>0)
    
    def test_mercado_trades_interval(self):
        m = Mercado('bch-cop')
        now = int(time.time())*1000
        current_timestamp = int(time.time())*1000
        yesterday = now - 60*60*24*1000
        m._getTrades(now, current_timestamp, [])
        trade_prices = m.getTradePrices()
        first_timestamp = int(m.trades[0][0])
        last_timestamp = int(m.trades[-1][0])
        print('now      : ', now)
        print('first ts : ', first_timestamp)
        print('yesterday: ', yesterday)
        print('last  ts : ', last_timestamp)
        self.assertTrue((first_timestamp <= now) and (last_timestamp >= yesterday))
        
if __name__ == '__main__':
    unittest.main()