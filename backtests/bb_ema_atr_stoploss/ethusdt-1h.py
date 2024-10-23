import pandas as pd
from backtesting import Backtest
from backtesting.lib import plot_heatmaps
from bb_ema_atr_stoploss import BBEmaAtrsl

df122 = pd.read_csv(
    "data\ETHUSDT_60_2022-01-01_2022-01-31.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df222 = pd.read_csv(
    "data\ETHUSDT_60_2022-02-01_2022-02-28.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df322 = pd.read_csv(
    "data\ETHUSDT_60_2022-03-01_2022-03-31.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df422 = pd.read_csv(
    "data\ETHUSDT_60_2022-04-01_2022-04-30.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df522 = pd.read_csv(
    "data\ETHUSDT_60_2022-05-01_2022-05-31.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df622 = pd.read_csv(
    "data\ETHUSDT_60_2022-06-01_2022-06-30.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df722 = pd.read_csv(
    "data\ETHUSDT_60_2022-07-01_2022-07-31.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df822 = pd.read_csv(
    "data\ETHUSDT_60_2022-08-01_2022-08-31.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df922 = pd.read_csv(
    "data\ETHUSDT_60_2022-09-01_2022-09-30.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df1022 = pd.read_csv(
    "data\ETHUSDT_60_2022-10-01_2022-10-31.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df1122 = pd.read_csv(
    "data\ETHUSDT_60_2022-11-01_2022-11-30.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df1222 = pd.read_csv(
    "data\ETHUSDT_60_2022-12-01_2022-12-31.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df123 = pd.read_csv(
    "data\ETHUSDT_60_2023-01-01_2023-01-31.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df223 = pd.read_csv(
    "data\ETHUSDT_60_2023-02-01_2023-02-28.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df323 = pd.read_csv(
    "data\ETHUSDT_60_2023-03-01_2023-03-31.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df423 = pd.read_csv(
    "data\ETHUSDT_60_2023-04-01_2023-04-30.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df523 = pd.read_csv(
    "data\ETHUSDT_60_2023-05-01_2023-05-31.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df623 = pd.read_csv(
    "data\ETHUSDT_60_2023-06-01_2023-06-30.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df723 = pd.read_csv(
    "data\ETHUSDT_60_2023-07-01_2023-07-31.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df823 = pd.read_csv(
    "data\ETHUSDT_60_2023-08-01_2023-08-31.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)
df923 = pd.read_csv(
    "data\ETHUSDT_60_2023-09-01_2023-09-30.csv",
    header=0,
    names=["Date", "Open", "High", "Low", "Close", "Volume"],
)

df_concat = pd.concat(
    [
        df122,
        df222,
        df322,
        df422,
        df522,
        df622,
        df722,
        df822,
        df922,
        df1022,
        df1122,
        df1222,
        # df123,
        # df223,
        # df323,
        # df423,
        # df523,
        # df623,
        # df723,
        # df823,
        # df923,
    ],
    ignore_index=True,
)

df_concat.index = pd.DatetimeIndex(df_concat["Date"])

bt = Backtest(df_concat, BBEmaAtrsl, cash=10000, commission=0.0003, margin=1)

stats = bt.optimize(
    bbLength=20,
    bbMult=2,
    emaLength=range(10, 100, 10),
    atrLength=14,
    atrMult=range(1, 5, 1),
    atrMultMult=range(1, 5, 1),
    maximize="Sharpe Ratio",
    constraint=lambda params: params.emaLength > params.bbLength,
)

stats = bt.run()

print(stats)

bt.plot()