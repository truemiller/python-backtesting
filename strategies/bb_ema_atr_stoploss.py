from backtesting import Strategy
from ta.volatility import BollingerBands, AverageTrueRange
from ta.trend import EMAIndicator


"""
This strategy combines Bollinger Bands, EMA (Exponential Moving Average), and ATR (Average True Range) to generate buy and sell signals with dynamic stop-loss and take-profit levels.

- **Bollinger Bands**:
  - Buy when price touches the lower Bollinger Band (oversold condition).
  - Sell when price touches the upper Bollinger Band (overbought condition).

- **Exponential Moving Average (EMA) Filter**:
  - Buy signals are allowed only when the price is above the 40-period EMA (bullish filter).
  - Sell signals are allowed only when the price is below the 40-period EMA (bearish filter).

- **Average True Range (ATR)**:
  - Used to set the stop-loss and take-profit levels dynamically based on market volatility.
  - Stop-loss is set as a multiple (`atrMult`) of the ATR.
  - Take-profit is set at a dynamic multiple of ATR (`atrMult + atrMultMult`).

- The position size is set to 0.5, meaning 50% of the available cash is used for each trade.
- This implementation uses stop-loss and take-profit for exit strategies instead of closing positions based on opposite signals.

Key Parameters:
- `bbLength` = 20: Bollinger Bands window length.
- `bbMult` = 2: Bollinger Bands multiplier.
- `emaLength` = 40: EMA window length.
- `atrLength` = 14: ATR window length.
- `atrMult` = 1: ATR multiplier for stop-loss.
- `atrMultMult` = 1: Additional multiplier for take-profit.
"""

class BbEmaAtrSl(Strategy):
    bbLength = 20  # Length for Bollinger Bands (20 periods)
    bbMult = 2  # Bollinger Bands multiplier (2 standard deviations)
    emaLength = 40  # Length for Exponential Moving Average (40 periods)
    atrLength = 14  # Length for Average True Range (14 periods)
    atrMult = 1  # ATR multiplier for stop-loss
    atrMultMult = 1  # Additional ATR multiplier for take-profit

    def init(self):
        """
        Initialize Bollinger Bands, EMA, and ATR indicators.
        Register them for plotting and use in strategy logic.
        """
        close = self.data.Close
        # Initialize Bollinger Bands with the specified length and multiplier
        self.bb = BollingerBands(close.s, self.bbLength, self.bbMult)
        self.bbU = self.I(self.bb.bollinger_hband)  # Upper Bollinger Band
        self.bbL = self.I(self.bb.bollinger_lband)  # Lower Bollinger Band

        # Initialize the EMA (Exponential Moving Average) with the specified window length
        self.ema = EMAIndicator(close=close.s, window=self.emaLength)
        self.emaL = self.I(self.ema.ema_indicator)  # EMA values

        # Initialize the ATR (Average True Range) for volatility-based stop-loss and take-profit
        self.atr = AverageTrueRange(self.data.High.s, self.data.Low.s, self.data.Close.s, self.atrLength)
        self.atrI = self.I(self.atr.average_true_range)  # ATR values

    def next(self):
        """
        Define the strategy logic for entering and managing positions.
        Positions are opened based on Bollinger Bands signals and filtered by EMA.
        Stop-loss and take-profit levels are dynamically set using ATR.
        """
        # Define sell signal when the price touches or exceeds the upper Bollinger Band
        signalSell = self.data.High > self.bbU
        # Define buy signal when the price touches or falls below the lower Bollinger Band
        signalBuy = self.data.Low < self.bbL

        # Filter for bullish conditions: Price is above EMA
        bullishFilter = self.data.Close > self.emaL
        # Filter for bearish conditions: Price is below EMA
        bearishFilter = self.data.Close < self.emaL

        # If no position is currently open, look for opportunities to enter
        if not self.position:
            # Sell signal: Upper Bollinger Band hit and below EMA (bearish trend)
            if signalSell and bearishFilter:
                self.sell(
                    size=0.5,  # Use 50% of available capital
                    sl=self.data.Close + (self.atrI * self.atrMult),  # Stop-loss based on ATR
                    tp=self.data.Close - (self.atrI * (self.atrMult + self.atrMultMult)),  # Take-profit based on ATR
                )
            # Buy signal: Lower Bollinger Band hit and above EMA (bullish trend)
            elif signalBuy and bullishFilter:
                self.buy(
                    size=0.5,  # Use 50% of available capital
                    sl=self.data.Close - (self.atrI * self.atrMult),  # Stop-loss based on ATR
                    tp=self.data.Close + (self.atrI * (self.atrMult + self.atrMultMult)),  # Take-profit based on ATR
                )

        # Uncomment the below block to close positions based on opposite signals
        # if self.position.is_long and signalSell and bearishFilter:
        #     self.position.close()  # Close long if sell signal occurs in bearish trend
        # elif self.position.is_short and signalBuy and bullishFilter:
        #     self.position.close()  # Close short if buy signal occurs in bullish trend
