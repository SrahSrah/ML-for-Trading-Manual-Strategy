# ML-for-Trading-Manual-Strategy
Explores how to beat the stock market with traditional metrics such as momentum and Bollinger Bands


**Indicators**:

For Project 6, I used three indicators: Momentum, Simple Moving Average, and Bollinger Bands. Each indicator is created by calling the gen\_ind1\_momentum(), gen\_ind2\_sma(), and gen\_ind3\_bollinger\_bands() methods, respectively. All indicators can be generated with a called  to the gen\_all\_indicators() method, and all indicators can be retrieved with a call to get\_all\_indicators().

Below is a normalized comparison of JPM vs. SPY during the in-sample period, for reference. As we can see, they have a fairly high correlation, buy SPY outperforms JPM handily in the end. 

<p align="center">
  <img src="Aspose.Words.955ac5df-74fc-4742-ac25-dac57f37029c.001.png"/>
</p>

1. **Momentum:**  

Momentum is defined as the change in value over a set number of n days. It represents the rate of the rise and fall of a stock, and can be calculated by dividing the day’s current price by the price n days ago, and subtracting one. The steepness of the slope represents the “strength” of the momentum. In my manual strategy, I use the slope of momentum over a set number of days to determine if we should buy or sell.

<p align="center">
  <img src="Aspose.Words.955ac5df-74fc-4742-ac25-dac57f37029c.002.png"/>
</p>
The graph above plots momentum and the normalized JPM price over the in-sample period. It is apparent that during periods of stability, the momentum in turn becomes less volatile, and vice-versa. Momentum will be a useful indicator for our manual strategy as momentum can give us an insight as to the current general direction of the stock. For example, if the slope of momentum over n days is positive, we can generally expect the stock to keep rising, and we thus buy. Consequently, should the slope of momentum be negative, we should sell to avoid large losses.

2. **Simple Moving Average:** 

The Simple Moving Average (SMA) of a stock is simply the moving average of a stock’s price over time, with a window of n days. The graph below shows SMA through our in-sample period. 

<p align="center">
  <img src="Aspose.Words.955ac5df-74fc-4742-ac25-dac57f37029c.003.png"/>
</p>
We can use the SMA to predict future prices by keeping track of when the price crosses the SMA line. If the price is lower than the SMA, an arbitrage opportunity appears, and we should buy the stock. Likewise, if the price creeps above the SMA, we should sell. In the manual strategy, I check which is larger: SMA or price (thus essentially checking Price/SMA), to determine the trades for that day.

3. **Bollinger Bands:** 

Related to SMA, the Upper and Lower Bollinger Bands are simply +/- 2 \* the rolling SMA standard deviation.  Show below over the in-sample period, I believe Bollinger Bands to be the most predictive of future price value.

<p align="center">
  <img src="Aspose.Words.955ac5df-74fc-4742-ac25-dac57f37029c.004.png"/>
</p>
It was mentioned above the theory that we should buy/sell if the price went below/above the SMA. While this is true, I would stipulate that first one must check if the price violates the bounds of the Bollinger Bands. Should the price fall below the lower band, one should buy to capitalize on the large arbitrage opportunity, and vice versa. It should be noted that the purchase should, in practice, be made once the price makes an indication of returning to the SMA, but I have omitted that stipulation from my code’s execution due to the 1 trade/day rule.

**Best Possible Strategy:** 

To calculate the best possible strategy, I simply peaked forward by one day. If the stock rose in price tomorrow, I would buy today. If the stock fell tomorrow, I would sell today. If the price held in magnitude, I would hold. I assumed that I could not see any dates outside of the in-sample range, and thus made no trades on the last day. The graph below shows the normalized results of my Theoretically Optimal Strategy described above and the benchmark case, wherein we buy 1000 shares on the first day and hold throughout the sample period.

<p align="center">
  <img src="Aspose.Words.955ac5df-74fc-4742-ac25-dac57f37029c.005.png"/>
</p>
**Manual Strategy:**  

For my manual strategy, I used a series of cascading if statements to determine whether we should buy, sell, or hold. Because the general trend of the economy is upward, I purchased stock if it was the first day of the sample. Each buy and sell order would buy or sell 100% of the stocks available to trade based on the assignment’s holding restrictions. After that, assuming I was not at a holdings boundary (+/- 1000 shares), I followed the following logic:

- Else If today’s price was lower than today’s lower Bollinger Band: BUY
- Else if today’s price was higher than today’s upper Bollinger Band: SELL
- Else if the slope of momentum over the past n days is above a threshold: BUY 
- Else if the slope of momentum over the past n days is below a threshold: SELL
- Else if SMA is higher than the price over m days: BUY
- Else if SMA is lower than the price over m days: SELL
- Else: HOLD

I placed the Bollinger Band if statements first as I believe those to have the largest arbitrage opportunities and should always be executed when possible. Should those conditions not be met, I then move onto checking the slope of momentum over n days. If the slope of momentum is positive and above a low threshold (0.075 in this case), I instruct the computer to BUY because when momentum is positive, we can reasonably expect the price to continue increasing. The opposite holds true for negative momentum slope: we SELL in that case because we expect the price to continue falling.

Lastly, I looked at the SMA. But I don’t just look at today’s SMA vs. today’s price, and that would be, in my opinion, too low a threshold to determine a trade. Rather, I check if the SMA is consistently higher or lower than the price. One day could be a fluke, but multiple days a trend makes. Thus, if the SMA is higher/lower than the price for three days straight, we BUY/SELL to capitalize on the deviation, as we can reasonably expect the price to return to the SMA. 

While this strategy is effective in the end, as it outperforms the benchmark for both in-sample and out-sample data (see figures below), it’s not by much, with both generating barely positive returns. This makes me question the validity of my strategy. However, interestingly, the manual strategy seems to perform best during the financial crisis of 2008-2009, potentially indicating that my strategy performs better during market downturns than upswings. 

Another point of interest is that my strategy appears to be negatively correlated to the benchmark for the entirety of the in-sample data. At first glance, the out-of-sample result appears to be the same way. But one important exception soon becomes evident: for the entire first half of 2011, both the benchmark and my strategy trend downward. Indeed, this appears to be the only span of time both metrics are positively correlated. Could this be indicative of sector downturn, rather than a market one?

Looking at the table of statistics for each result below, the benchmarks for both in and out- sample data had negative Sharpe Ratios. Both resultant manual strategies, however, had positive Sharpe Ratio, with the in-sample results having an impressive ratio of 0.209. The same pattern holds for cumulative returns and average daily return, in which the both benchmarks are negative but both manual strategy results are positive. Both manual strategies have a lower standard deviation of returns than their benchmark counterparts, which in theory reduces volatile and is a good sign, but the magnitude of these values is so small this trend may be insignificant. Finally, both bench markets have a lower final portfolio value than the starting value, while both manual strategies have a higher final portfolio value.

In conclusion, though my strategy outperforms the benchmark for both in and out-sample data, returns are never more than marginal. The poor performance of the benchmark, essentially one LONG purchase, in both cases suggests that anything more than a marginal performance would be difficult regardless. 

I look forward to adding machine learning to the mix!

<p align="center">
  <img src="Aspose.Words.955ac5df-74fc-4742-ac25-dac57f37029c.006.png"/>
</p>
<p align="center">
  <img src="Aspose.Words.955ac5df-74fc-4742-ac25-dac57f37029c.007.png"/>
</p>
Table 1: Summary of Statistics for In-Sample and Out-Sample Data:



||**In-Sample**|**Out-Sample**|
| :- | - | - |
||**Benchmark**|**Manual Strategy**|**Benchmark**|**Manual Strategy**|
|**Sharpe Ratio**|-0.06109401359|0.2091677482|-0.5136886344|0.09349204313|
|**Cumulative Return**|-0.00378556582|0.009957214344|-0.01334771041|0.002234228795|
|**Average Daily Return**|-6.22E-06|2.09E-05|-2.64E-05|4.76E-06|
|**Standard Deviation of Return**|0.00161657455|0.001587422147|0.0008153073|0.000808782527|
|**Final Value**|0.9962144342|1.009957214|0.9866522896|1.002234229|


