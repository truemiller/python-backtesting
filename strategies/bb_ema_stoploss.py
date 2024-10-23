from backtesting import Strategy
from ta.volatility import BollingerBands
from ta.trend import EMAIndicator

"""
This strategy combines Bollinger Bands (BB) and Exponential Moving Average (EMA) filters to generate buy and sell signals with a dynamic stop-loss.

- Bollinger Bands:
  - A 20-period Bollinger Band is used with a multiplier of 2.
  - Buy signal: When the price touches or falls below the lower Bollinger Band.
  - Sell signal: When the price touches or exceeds the upper Bollinger Band.

- Exponential Moving Average (EMA) Filter:
  - A 60-period EMA is used as a trend filter.
  - Buy signals are only allowed when the price is above the EMA (bullish filter).
  - Sell signals are only allowed when the price is below the EMA (bearish filter).

- Stop-Loss:
  - The stop-loss is dynamically adjusted based on the percentage distance from the entry price.
  - Optimized stop-loss values range between 0.5% and 5%.
"""

# Define the custom strategy
class BbEmaSl(Strategy):
    bbLength = 20  # Bollinger Bands length (default 20 periods)
    bbMult = 2  # Bollinger Bands multiplier (default 2 standard deviations)
    emaLength = 60  # EMA length (default 60 periods)
    stopLoss = 0.005  # Stop-loss as a percentage of the entry price

    # Initialize Bollinger Bands and EMA indicators
    def init(self):
        close = self.data.Close
        self.bb = BollingerBands(close.s, self.bbLength, self.bbMult)  # Bollinger Bands
        self.bbU = self.I(self.bb.bollinger_hband)  # Upper Bollinger Band
        self.bbL = self.I(self.bb.bollinger_lband)  # Lower Bollinger Band
        self.ema = EMAIndicator(close=close.s, window=self.emaLength)  # EMA
        self.emaL = self.I(self.ema.ema_indicator)  # EMA values

    # Define the strategy logic
    def next(self):
        signalSell = self.data.High > self.bbU  # Price touches upper Bollinger Band
        signalBuy = self.data.Low < self.bbL  # Price touches lower Bollinger Band

        bullishFilter = self.data.Close > self.emaL  # Price is above the EMA (bullish)
        bearishFilter = self.data.Close < self.emaL  # Price is below the EMA (bearish)

        # If no current position, check for new buy or sell opportunities
        if not self.position:
            if signalSell and bearishFilter:
                # Open a short position with a stop-loss
                self.sell(sl=self.data.Close * (1 + self.stopLoss))
            elif signalBuy and bullishFilter:
                # Open a long position with a stop-loss
                self.buy(sl=self.data.Close * (1 - self.stopLoss))
        # If already in a position, check if it needs to be closed
        else:
            if self.position.is_long and signalSell:
                self.position.close()  # Close long if price hits upper BB
            elif self.position.is_short and signalBuy:
                self.position.close()  # Close short if price hits lower BB
