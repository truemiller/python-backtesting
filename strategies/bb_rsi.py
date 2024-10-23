from backtesting import Strategy

from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator


"""
This strategy combines Bollinger Bands and RSI to generate buy and sell signals on AVAX/USDT 1-minute data.

- Bollinger Bands (BB):
  - A 20-period Bollinger Band is used with a multiplier of 2 (default settings).
  - Buy signal: When the price touches or falls below the lower Bollinger Band (oversold condition).
  - Sell signal: When the price touches or exceeds the upper Bollinger Band (overbought condition).

- RSI (Relative Strength Index):
  - A 14-period RSI is used to confirm overbought and oversold conditions.
  - Buy signal: RSI value below 20 (indicating oversold).
  - Sell signal: RSI value above 80 (indicating overbought).

- Trade Entry:
  - A buy trade is opened when both the price touches the lower BB and RSI is below 20.
  - A sell trade is opened when both the price touches the upper BB and RSI is above 80.
  
- Trade Exit:
  - Long positions are closed if a sell signal occurs, and short positions are closed if a buy signal occurs.

The strategy is backtested using AVAX/USDT 1-minute data, and Bollinger Band and RSI lengths are optimized for return.
"""

# Define the custom strategy
class BbRsi(Strategy):
    bbLength = 20  # Bollinger Bands length (default 20 periods)
    bbMult = 2  # Bollinger Bands multiplier (default 2 standard deviations)
    stopLoss = 0.005  # Stop loss level (not used directly in the code)
    rsiLength = 14  # RSI length (default 14 periods)

    # Initialize Bollinger Bands and RSI indicators
    def init(self):
        close = self.data.Close
        self.bb = BollingerBands(close.s, self.bbLength, self.bbMult)  # Bollinger Bands
        self.rsi = RSIIndicator(close.s, self.rsiLength)  # RSI Indicator
        self.bbU = self.I(self.bb.bollinger_hband)  # Upper Bollinger Band
        self.bbL = self.I(self.bb.bollinger_lband)  # Lower Bollinger Band
        self.rsiI = self.I(self.rsi.rsi)  # RSI values

    # Define the strategy logic
    def next(self):
        signalSell = self.data.High > self.bbU  # Price touches upper Bollinger Band
        signalBuy = self.data.Low < self.bbL  # Price touches lower Bollinger Band

        rsiSell = self.rsiI > 80  # RSI is above 80 (overbought)
        rsiBuy = self.rsiI < 20  # RSI is below 20 (oversold)

        # If no current position, check for new buy or sell opportunities
        if not self.position:
            if signalSell and rsiSell:
                self.sell()  # Open a short position if overbought
            elif signalBuy and rsiBuy:
                self.buy()  # Open a long position if oversold
        # If already in a position, check if it needs to be closed
        else:
            if self.position.is_long and signalSell:
                self.position.close()  # Close long if overbought
            elif self.position.is_short and signalBuy:
                self.position.close()  # Close short if oversold


