from backtesting import Strategy

from ta.trend import SMAIndicator


"""
This strategy uses a 133-period Simple Moving Average (SMA) to detect buying opportunities based on recent price momentum.

- The strategy checks if the current closing price is above the 133-period SMA.
- It then looks back at the closing prices from 18 and 36 periods ago:
  - Buy signal 1: The price increase over the past 18 periods must exceed the "extreme" threshold (-0.005 by default, meaning no significant price drop).
  - Buy signal 2: The current price must be greater than the price 36 periods ago.

- If both signals are satisfied and there is no open position, a buy order is placed.
- Each buy sets a take-profit (TP) target of 0.75% and a stop-loss (SL) at 0.5%.

The strategy is backtested using ETH/USDT 15-minute data, with no leverage and no commission.
"""

# Define the custom strategy
class SmaLookback(Strategy):
    sma = 133  # 133-period SMA for trend detection
    backLong = 18  # Lookback period for price comparison (18 periods)
    backShort = 18  # Shorter lookback period for signal calculation
    extreme = -0.005  # Threshold for price increase check

    # Initialize indicators
    def init(self):
        close = self.data.Close
        self.sma = SMAIndicator(close=close, window=self.sma, fillna=True)  # 133-period SMA

    # Define the logic for each trading step
    def next(self):
        # Ensure there are at least 36 periods of data to evaluate signals
        if len(self.data.Close) > 36:
            # Check if the current price is above the 133-period SMA
            if self.sma and self.data.Close > self.sma.sma_indicator():
                # Look back at the price 18 and 36 periods ago
                buyLookback1 = self.data.Close[-self.backLong]
                buyLookback2 = self.data.Close[-(self.backLong * 2)]
                # Check buy signal 1: Price must not have dropped significantly in 18 periods
                signalBuy1 = ((self.data.Close / buyLookback1) - 1) > self.extreme
                # Check buy signal 2: Current price must be higher than 36 periods ago
                signalBuy2 = self.data.Close > buyLookback2

            # If there's no open position and both buy signals are triggered
            if not self.position:
                if signalBuy1 and signalBuy2:
                    # Place a buy order with TP at 0.75% and SL at 0.5%
                    self.buy(
                        size=1,
                        tp=self.data.Close * 1.0075,  # Take profit at 0.75% gain
                        sl=self.data.Close * 0.995,  # Stop loss at 0.5% loss
                    )

