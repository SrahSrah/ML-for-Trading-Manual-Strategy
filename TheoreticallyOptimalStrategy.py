"""
Implements the theoretically optimal strategy of stock as if we could see into the future

-Provides a chart of the benchmark vs. optimal strategyselfself.
-Also reports the cr, std of dr's, and mean of dr's for symbol_to_path

"""

from util import get_data
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import pandas as pd
import marketsimcode as ms


class TheoreticallyOptimalStrategy():

    def __init__(self):
        pass

    def author():
        return "shernandez43"

    def testPolicy(self, symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
        dates = pd.date_range(sd, ed)
        data = get_data([symbol], dates)
        self.data = data[[symbol]]
        self.symbol = symbol
        self.normed_data = data/data.iloc[0]

        benchmark = self.gen_benchmark()
        cols = ["Symbol", "Order", "Shares"]


        # create ideal trades using only +/- 1000 and 0 holdings:
        ideal_trades = np.zeros(shape = (self.data.shape[0],3))
        ideal_trades = pd.DataFrame(ideal_trades, index = self.data.index.values, columns = cols)
        holdings = 0    # initial holdsing value:
        for i in range(self.data.shape[0]-1):
            # if stock goes up the next day, buy:
            if self.data[symbol].ix[i+1] > self.data[symbol].ix[i] and holdings < 1000:
                to_buy = 1000 - holdings
                ideal_trades.ix[i] = ("JPM", "BUY", to_buy)
                holdings = holdings + to_buy
            # if stock goes down the next day, sell:
            elif self.data[symbol].ix[i+1] < self.data[symbol].ix[i] and holdings > -1000:
                to_sell = 1000 + holdings
                ideal_trades.ix[i] = ("JPM", "SELL", to_sell)
                holdings = holdings - to_sell


        benchmark["Symbol"] = self.symbol
        ideal_trades["Symbol"] = self.symbol


        # create bench trades df:
        dummy = benchmark.copy()
        dummy[self.symbol] = benchmark["Shares"]
        bench_trades = dummy[self.symbol]
        bench_trades = bench_trades.to_frame()


        #create trades df in the required format: +/- trade volume based on buy/sell
        dummy = ideal_trades.copy()
        dummy[self.symbol] = ideal_trades["Shares"]
        dummy.loc[dummy["Order"] == "SELL", self.symbol] *= -1

        trades = dummy[self.symbol]
        trades = trades.to_frame()


        self.plot(bench_trades, trades)


        return trades



    def gen_benchmark(self):
        columns = ["Symbol", "Order",
        "Shares"]
        index = self.data.index.values
        trades = np.zeros(shape = (len(index), len(columns)), dtype = object)
        trades[0][0], trades[0][1], trades[0][2] = self.symbol, "BUY", 1000
        trades = pd.DataFrame(trades, index = index, columns = columns)
        trades.rename(columns = {trades.columns.values[0] : self.symbol})
        return trades



    def plot(self, benchmark, ideal_trades):
        ideal_port = ms.compute_portvals(ideal_trades, commission=0.0, impact=0.0)
        bench_port = ms.compute_portvals(benchmark, commission=0.0, impact=0.0)
        ideal_port = ideal_port/ideal_port.iloc[0]
        bench_port = bench_port/bench_port.iloc[0]
        ms.get_port_stats(ideal_port, "Normalized Ideal Portfolio")
        ms.get_port_stats(bench_port, "Normalized Benchmark Portfolio")
        plt.plot(bench_port, label = "Benchmark", color = 'green')
        plt.plot(ideal_port, label = "Theoretically Optimal Strategy", color = 'red')
        plt.title("Theoretically Optimal Strategy vs. Benchmark")
        plt.legend()

        plt.savefig("TheoreticallyOptimalStrategy.png")


if __name__ == "__main__":
    tos = TheoreticallyOptimalStrategy()
    df_trades = tos.testPolicy()
