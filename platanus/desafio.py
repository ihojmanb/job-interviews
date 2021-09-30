import requests 
from datetime import datetime
import time

def timestampToDate(timestamp):
    dt_object = datetime.fromtimestamp(timestamp/1000)
    return dt_object
class BudaBot():
    # val=False means 'don't initialize Mercados'
    # its just for testing purposes
    # when using de BudaBot class, instance it like BudaBot(init_markets=True)

    def __init__(self,init_markets=False):
        self.mercadosId = self._getMercadosId()
        self.mercados = self._getMercados(init_markets)
        

    # returns a list with every market-id
    def _getMercadosId(self):
        url = 'https://www.buda.com/api/v2/markets'
        response = requests.get(url)
        marketObj = response.json()
        marketArr =  marketObj['markets']
        marketIdList = list(map(lambda o: o['id'], iter(marketArr)))
        return marketIdList

    def getMercadosId(self):
        return self.mercadosId
    # returns a list of Mercado objects based on market-id's list
    def _getMercados(self, val):
        return list(map(lambda i: Mercado(i, initialize=val), iter(self.getMercadosId())))

    def getMercados(self):
        return self.mercados
    
    def getMercadosMaxPrices(self):
        return (list(map(lambda m: m.getMaxTradePrice(), iter(self.getMercados()))))


class Mercado():
    __slots__ = ["market_id", "trades", "tradePrices", "maxTradePrice","first_timestamp", "last_timestamp"]
    def __init__(self, id, initialize=True):
        if(initialize):
            self.market_id = id
            self.trades = self._getTrades(int(time.time())*1000, int(time.time())*1000, [])
            self.tradePrices = self._getTradePrices()
            self.maxTradePrice = self._getMaxTradePrice()
        else:
            self.market_id = id
            self.trades = []
            self.tradePrices = []
            self.maxTradePrice = None
    
    # gets trade from now up to the last 24 hrs. Returns a list
    # with every trade entry between the 24hr interval
    def _getTrades(self, now, current_ts, trades_list):
        market_id = self.market_id
        url = f'https://www.buda.com/api/v2/markets/{market_id}/trades'
        response = requests.get(url, params={
            'timestamp': current_ts, 'limit': 100})
        trades = response.json()   
        last_timestamp = int(trades['trades']['last_timestamp'])
        yesterday = now - 60*60*24*1000
        if current_ts <= yesterday:
            # cleans the entries that the last function-call add to the list
            # which are not part od the 24hr interval
            self.trades = list(filter(lambda x: int(x[0])>=yesterday, iter(trades_list)))
            # saving final trade timestamp interval
            self.first_timestamp = timestampToDate(int(self.trades[0][0]))
            self.last_timestamp = timestampToDate(int(self.trades[-1][0]))
            return trades_list
        else:
            new_entries_list = trades['trades']['entries']
            updated_list = trades_list + new_entries_list
            return self._getTrades(now, last_timestamp, updated_list)
    
    def getTrades(self):
        return self.trades
    def _getTradePrices(self):
        return list(map(lambda o: float(o[2]), iter(self.trades)))

    def getTradePrices(self):
        return self.tradePrices

    def _getMaxTradePrice(self):
        return max(self.tradePrices)

    def getMaxTradePrice(self):
        return self.maxTradePrice

    def getMarketBrief(self):
        mid = self.market_id
        fts = self.first_timestamp
        lts = self.last_timestamp
        maxprice = self.maxTradePrice
        brief =  """Market Brief - last 24 hours
        market: {}
        first trade datetime : {}
        last trade datetime  : {}
        ---------------------
        maximum trade price  : {}
        ---------------------
        """.format(mid, fts, lts, maxprice)
        print(brief)


if __name__ == "__main__":
    print('Loading Markets... Please Wait\n')
    budabot = BudaBot(init_markets=True)
    for m in budabot.getMercados():
        m.getMarketBrief()





