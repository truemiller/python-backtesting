import pandas as pd
from backtesting import Backtest
from backtesting.lib import plot_heatmaps
from bb_ema_atr_stoploss import BBEmaAtrsl

df1 = pd.read_csv(
    "data\AVAXUSDT_1_2023-01-01_2023-01-31.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df2 = pd.read_csv(
    "data\AVAXUSDT_1_2023-02-01_2023-02-28.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df3 = pd.read_csv(
    "data\AVAXUSDT_1_2023-03-01_2023-03-31.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df4 = pd.read_csv(
    "data\AVAXUSDT_1_2023-04-01_2023-04-30.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df5 = pd.read_csv(
    "data\AVAXUSDT_1_2023-05-01_2023-05-31.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)


df_concat = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)
df_concat.index = pd.DatetimeIndex(df_concat["Date"])
print(df_concat)
bt = Backtest(df3, BBEmaAtrsl, cash=10000, commission=0.0006, margin=1)

stats, heatmap = bt.optimize(
    atrLength=range(5, 25, 5),
    atrMult=range(1, 4, 1),
    bbLength=range(5, 25, 5),
    emaLength=range(10, 100, 10),
    maximize="Return [%]",
    return_heatmap=True,
    constraint=lambda params: params.emaLength > params.bbLength,
)

print(stats)
print(stats._strategy)

bt.plot(plot_pl=False, plot_volume=False)
plot_heatmaps(
    heatmap=heatmap,
)
