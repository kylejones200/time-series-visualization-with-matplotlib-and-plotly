from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def make_synthetic_series(cfg: dict[str, Any]) -> pd.DataFrame:
    """Build the synthetic daily series used in the article examples."""
    data_cfg = cfg.get("data") or {}
    seed = int(data_cfg.get("seed", 42))
    periods = int(data_cfg.get("periods", 100))
    start = str(data_cfg.get("start", "2023-01-01"))
    freq = str(data_cfg.get("freq", "D"))
    window = int(data_cfg.get("moving_average_window", 7))

    rng = np.random.default_rng(seed)
    time = pd.date_range(start=start, periods=periods, freq=freq)
    values = (
        100
        + 2 * np.arange(periods)
        + np.sin(np.linspace(0, 10, periods)) * 10
        + rng.normal(0, 5, periods)
    )
    df = pd.DataFrame({"Date": time, "Value": values})
    df["Moving_Avg"] = df["Value"].rolling(window=window).mean()
    df["Day_of_Week"] = df["Date"].dt.day_name()
    df["Value_2"] = df["Value"] + rng.normal(0, 10, len(df))
    return df
