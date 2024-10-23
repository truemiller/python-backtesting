import pandas as pd

from backtesting import Backtest, Strategy
from backtesting.lib import plot_heatmaps

from ta.volatility import BollingerBands, AverageTrueRange


"""
This strategy uses Bollinger Bands (BB) and Average True Range (ATR) to generate buy and sell signals with volatility-based stop-loss levels.

- Bollinger Bands:
  - A 20-period Bollinger Band is used with a multiplier of 2 by default.
  - Buy signal: When the price touches or falls below the lower Bollinger Band (indicating an oversold condition).
  - Sell signal: When the price touches or exceeds the upper Bollinger Band (indicating an overbought condition).

- Average True Range (ATR):
  - A 20-period ATR is used to adjust the stop-loss level based on market volatility.
  - The stop-loss is set at a distance of 3 times the ATR from the entry price.

- Trade Entry:
  - A buy trade is opened when the price touches the lower Bollinger Band with a stop-loss based on the ATR.
  - A sell trade is opened when the price touches the upper Bollinger Band with a stop-loss based on the ATR.

- Trade Exit:
  - Long positions are closed if a sell signal occurs.
  - Short positions are closed if a buy signal occurs.

The strategy is backtested using AVAX/USDT 1-minute data, and the Bollinger Band and ATR lengths are optimized for return.
"""

# Define the custom strategy
class BbCrossAtr(Strategy):
    bbLength = 20  # Bollinger Bands length (default 20 periods)
    bbMult = 2  # Bollinger Bands multiplier (default 2 standard deviations)
    emaLength = 40  # EMA length (not used in the logic, can be removed for now)
    atrLength = 20  # ATR length (default 20 periods)
    atrMult = 3  # Multiplier for ATR-based stop-loss

    # Initialize Bollinger Bands and ATR indicators
    def init(self):
        close = self.data.Close
        self.bb = BollingerBands(close.s, self.bbLength, self.bbMult)  # Bollinger Bands
        self.bbU = self.I(self.bb.bollinger_hband)  # Upper Bollinger Band
        self.bbL = self.I(self.bb.bollinger_lband)  # Lower Bollinger Band
        self.atr = AverageTrueRange(
            self.data.High.s, self.data.Low.s, self.data.Close.s, self.atrLength
        )  # Average True Range for volatility
        self.atrI = self.I(self.atr.average_true_range)  # ATR values

    # Define the strategy logic
    def next(self):
        signalSell = self.data.High > self.bbU  # Price touches upper Bollinger Band
        signalBuy = self.data.Low < self.bbL  # Price touches lower Bollinger Band

        # If no current position, check for new buy or sell opportunities
        if not self.position:
            if signalSell:
                # Open a short position with ATR-based stop-loss
                self.sell(sl=self.data.Close + (self.atrI * self.atrMult))
            elif signalBuy:
                # Open a long position with ATR-based stop-loss
                self.buy(sl=self.data.Close - (self.atrI * self.atrMult))
        # If already in a position, check if it needs to be closed
        else:
            if self.position.is_long and signalSell:
                self.position.close()  # Close long if price touches upper BB
            elif self.position.is_short and signalBuy:
                self.position.close()  # Close short if price touches lower BB
