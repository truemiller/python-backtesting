import pandas as pd
from backtesting import Backtest
from backtesting.lib import plot_heatmaps
from strategies.sma_crossover import SmaCrossover

# Load historical ETH/USDT data for backtesting
df1 = pd.read_csv(
    "data//ETHUSDT_15_2023-01-01_2023-01-31.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df2 = pd.read_csv(
    "data//ETHUSDT_15_2023-02-01_2023-02-28.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df3 = pd.read_csv(
    "data//ETHUSDT_15_2023-03-01_2023-03-31.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df4 = pd.read_csv(
    "data//ETHUSDT_15_2023-04-01_2023-04-30.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df5 = pd.read_csv(
    "data//ETHUSDT_15_2023-05-01_2023-05-31.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)

# Concatenate all dataframes into a single dataset
data = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)

# Initialize the backtest with the combined dataset and strategy
bt = Backtest(
    data,
    SmaCrossover,  # Strategy class
    cash=10000,  # Initial capital
    commission=0.008,  # 0.8% commission per trade
    margin=1,  # No leverage
)

# Optimize strategy parameters (fastSmaWindow and slowSmaWindow) to maximize win rate
stats = bt.optimize(
    fastSmaWindow=range(10, 100, 10),  # Test fast SMA windows from 10 to 90
    slowSmaWindow=range(10, 200, 10),  # Test slow SMA windows from 10 to 190
    maximize="Win Rate [%]",  # Optimize for highest win rate
    constraint=lambda params: params.fastSmaWindow > params.slowSmaWindow,  # Ensure fast SMA < slow SMA
)

# Print optimization results
print(stats)
print(stats._strategy)

# Plot the backtest results
bt.plot()

# Optional plotting commands for further analysis
# bt.plot(plot_pl=False, plot_volume=False)  # Example: plot without PnL and volume
# plot_heatmaps(heatmap=heatmap, agg="mean")  # Example: plot heatmaps for analysis
