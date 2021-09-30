import requests 
from datetime import datetime
import time
import plotly.express as px
from desafio import *

if __name__ == "__main__":
    print('Loading Markets... Please Wait\n')
    budabot = BudaBot(init_markets=True)
    for m in budabot.getMercados():
        m.getMarketBrief()

    x = budabot.getMercadosId()
    y = budabot.getMercadosMaxPrices()
    fig = px.scatter(x=x, y=y)
    fig.show()




