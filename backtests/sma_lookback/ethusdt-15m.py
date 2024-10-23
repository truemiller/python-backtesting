import pandas as pd
from backtesting import Backtest
from backtesting.lib import plot_heatmaps
from strategies.sma_lookback import SmaLookback


# Load historical ETH/USDT 15-minute data for backtesting
df1 = pd.read_csv(
    "../../data/ETHUSDT_15m_2021-01-01_2022-01-01.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)

# Initialize and run the backtest
bt = Backtest(df1, SmaLookback, cash=10000, commission=0.0000, margin=1)

# Run the backtest and plot the results
bt.run()
bt.plot()

# Optional: Uncomment to run parameter optimization
# stats = bt.optimize(
#     sma=[50, 100],  # Test different SMA window sizes
#     maximize="Return [%]",  # Maximize overall return
#     return_heatmap=True,  # Return heatmap for analysis
# )
# print(stats)
# print(stats._strategy)

# Optional plotting commands
# bt.plot(plot_pl=False, plot_volume=False)  # Example: plot without PnL and volume
# plot_heatmaps(heatmap=heatmap, agg="mean")  # Example: plot heatmaps for optimization
