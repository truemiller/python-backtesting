from backtesting import Strategy
from backtesting.lib import crossover

from ta.trend import SMAIndicator
from ta.momentum import RSIIndicator


"""
This strategy uses two Simple Moving Averages (SMA) to generate buy and sell signals on ETH/USDT 15-minute data.

- Buy signal: When the fast SMA (default 100-period) crosses above the slow SMA (default 200-period), indicating bullish momentum.
- Sell signal: When the fast SMA crosses below the slow SMA, indicating bearish momentum.

- A take-profit (TP) is set at 5%, and a stop-loss (SL) at 1% per trade to manage risk and reward.

The RSI is calculated but not used in the strategy logic, left in for visuals in report.

Backtested on ETH/USDT data, and the fast/slow SMA window parameters are optimized to maximize the win rate.
"""

# Define crossunder function for opposite of crossover
def crossunder(series1, series2):
    return crossover(series2, series1)


# Define the strategy
class SmaCrossover(Strategy):
    fastSmaWindow = 100  # Fast SMA window default
    slowSmaWindow = 200  # Slow SMA window default
    tp = 0.05  # Take profit at 5%
    sl = 0.01  # Stop loss at 1%

    # Initialize indicators
    def init(self):
        # Fast and slow SMA indicators
        self.fsma = SMAIndicator(
            close=self.data.Close.s, window=self.fastSmaWindow, fillna=True
        )
        self.ssma = SMAIndicator(
            close=self.data.Close.s, window=self.slowSmaWindow, fillna=True
        )

        # RSI indicator (currently not used in logic)
        self.rsi = RSIIndicator(close=self.data.Close.s, window=14)

        # Register indicators for plotting and strategy use
        self.rsiI = self.I(self.rsi.rsi)
        self.fsmaI = self.I(self.fsma.sma_indicator)
        self.ssmaI = self.I(self.ssma.sma_indicator)

    # Define strategy's trading logic
    def next(self):
        # Buy when fast SMA crosses above slow SMA (bullish crossover)
        if crossover(self.fsmaI, self.ssmaI):
            self.buy(
                sl=self.data.Close * (1 - self.sl),  # Set stop-loss
                tp=self.data.Close * (1 + self.tp),  # Set take-profit
            )
        # Sell when fast SMA crosses below slow SMA (bearish crossunder)
        if crossunder(self.fsmaI, self.ssmaI):
            self.sell(
                sl=self.data.Close * (1 + self.sl),  # Set stop-loss
                tp=self.data.Close * (1 - self.tp),  # Set take-profit
            )


