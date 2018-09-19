
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from collections import defaultdict


class QTrader(object):
    def __init__(self):
        self.stock_data = pd.merge(pd.read_csv('GSPC.csv', index_col='Date'), pd.read_csv('tbills.csv',index_col='Date'),\
                                   right_index=True, left_index=True).sort_index()
        self.returns = pd.DataFrame({
            'stocks': self.stock_data['Adj Close'].rolling(window=2).apply(lambda x : x[1]/x[0]-1),
            'tbills': (self.stock_data['tbill_rate']/100 + 1)**(1/52) -1 ,
        }, index = self.stock_data.index)
        self.returns['risk_adjusted'] = self.returns.stocks - self.returns.tbills

    def buy_and_hold(self, dates):
        return pd.Series(1, index = dates)

    def buy_tbills(self, dates):
        return pd.Series(0, index = dates)


    def random(self,dates):
        return pd.Series(np.random.randint(-1,2, size=len(dates)), index = dates)

    def evaluate(self, holdings):
        return pd.Series(self.returns.tbills + holdings * self.returns.risk_adjusted + 1, index=holdings.index).cumprod()

    def graph_portfolio(self):
        midpoint = int(len(self.returns.index)/2)
        training_index = self.returns.index[:midpoint]
        testing_index = self.returns.index[midpoint:]

        portfolios = pd.DataFrame({
            'buy_and_hold': self.evaluate(self.buy_and_hold(testing_index)),
            'buy_tbills': self.evaluate(self.buy_tbills(testing_index)),
            'random': self.evaluate(self.random(testing_index))
            # 'qtrader': self.evaluate(self.q_holdings(training_index, testing_index))
        }, index = testing_index)
        portfolios.plot()
        # plt.annotate("Buy and hold sharp ratio: {} \n QTrader: {}".format(self.sharp(portfolio.buy_and_hold),\
                                    # self.sharpe(portfolio.qtrader)), xy = (0.25,0.95), xycoords="axes fraction")
        plt.show()
