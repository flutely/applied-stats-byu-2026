import polars as pl
from plotnine import *

df = pl.read_parquet("data/utah-crash-data-2020.parquet")

hourly = (
    df
    .filter(pl.col("CRASH_DATETIME").is_not_null())
    .with_columns(pl.col("CRASH_DATETIME").dt.hour().alias("hour"))
    .group_by("hour")
    .agg(pl.len().alias("n_crashes"))
    .sort("hour")
)

p = (
    ggplot(hourly.to_pandas(), aes(x="hour", y="n_crashes"))
    + geom_col(fill="#2c7bb6", width=0.8)
    + scale_x_continuous(breaks=range(0, 24, 2))
    + scale_y_continuous(labels=lambda l: [f"{int(v/1000)}k" for v in l])
    + labs(
        title="Utah Crashes by Hour of Day (2016–2019)",
        x="Hour of Day",
        y="Number of Crashes",
    )
    + theme_bw()
    + theme(figure_size=(10, 4))
)

p
