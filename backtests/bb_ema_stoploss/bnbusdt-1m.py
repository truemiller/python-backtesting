import pandas as pd
from backtesting import Backtest
from backtesting.lib import plot_heatmaps
from strategies.bb_ema_stoploss import BbEmaSl

# Load historical BNB/USDT 1-minute data for backtesting
df1 = pd.read_csv(
    "data\BNBUSDT_1_2023-01-01_2023-01-31.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df2 = pd.read_csv(
    "data\BNBUSDT_1_2023-02-01_2023-02-28.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df3 = pd.read_csv(
    "data\BNBUSDT_1_2023-03-01_2023-03-31.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df4 = pd.read_csv(
    "data\BNBUSDT_1_2023-04-01_2023-04-30.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df5 = pd.read_csv(
    "data\BNBUSDT_1_2023-05-01_2023-05-31.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)

# Concatenate the dataframes into a single dataset and index by date
df_concat = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)
df_concat.index = pd.DatetimeIndex(df_concat["Date"])

# Print concatenated data for verification
print(df_concat)

# Initialize and run the backtest
bt = Backtest(df_concat, BbEmaSl, cash=10000, commission=0.0001, margin=1)

# Optimize strategy stop-loss values for maximum return
stats, heatmap = bt.optimize(
    stopLoss=[0.0025, 0.005, 0.1, 0.15, 0.2],  # Range of stop-loss percentages to test
    maximize="Return [%]",  # Maximize return
    return_heatmap=True,  # Return heatmap for visualization
)

# Print optimization results and strategy configuration
print(stats)
print(stats._strategy)

# Plot the heatmap of stop-loss optimizations
plot_heatmaps(heatmap=heatmap)
