from backtesting import Strategy

from ta.volatility import BollingerBands


"""
This strategy utilizes Bollinger Bands to generate buy and sell signals based on price crossing the upper and lower bands.

- Bollinger Bands (BB):
  - A 20-period Bollinger Band is used with a multiplier of 2 (default settings).
  - Buy signal: When the price touches or falls below the lower Bollinger Band (indicating an oversold condition).
  - Sell signal: When the price touches or exceeds the upper Bollinger Band (indicating an overbought condition).

- Trade Entry:
  - A buy trade is opened when the price touches the lower BB.
  - A sell trade is opened when the price touches the upper BB.

- Trade Exit:
  - Long positions are closed if the price falls below the middle Bollinger Band.
  - Short positions are closed if the price rises above the middle Bollinger Band.

The strategy is backtested using AVAX/USDT 1-minute data, and the Bollinger Band length is optimized to maximize return.
"""

# Define the custom strategy
class BbCross(Strategy):
    bbLength = 20  # Bollinger Bands length (default 20 periods)
    bbMult = 2  # Bollinger Bands multiplier (default 2 standard deviations)
    stopLoss = 0.005  # Stop loss level (not used directly in the code)

    # Initialize Bollinger Bands indicators
    def init(self):
        close = self.data.Close
        self.bb = BollingerBands(close.s, self.bbLength, self.bbMult)  # Bollinger Bands
        self.bbM = self.I(self.bb.bollinger_mavg)  # Middle Bollinger Band
        self.bbU = self.I(self.bb.bollinger_hband)  # Upper Bollinger Band
        self.bbL = self.I(self.bb.bollinger_lband)  # Lower Bollinger Band

    # Define the strategy logic
    def next(self):
        signalSell = self.data.High > self.bbU  # Price touches upper Bollinger Band
        signalBuy = self.data.Low < self.bbL  # Price touches lower Bollinger Band

        # If no current position, check for new buy or sell opportunities
        if not self.position:
            if signalSell:
                self.sell()  # Open a short position if price hits upper BB
            elif signalBuy:
                self.buy()  # Open a long position if price hits lower BB
        # If already in a position, check if it needs to be closed
        else:
            if self.position.is_long and self.data.Close < self.bbM:
                self.position.close()  # Close long if price falls below middle BB
            elif self.position.is_short and self.data.Close > self.bbM:
                self.position.close()  # Close short if price rises above middle BB