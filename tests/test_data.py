from __future__ import annotations

import yaml

from ts_viz_plotly.data import make_synthetic_series
from ts_viz_plotly.paths import DEFAULT_CONFIG_PATH


def test_synthetic_series_shape() -> None:
    with DEFAULT_CONFIG_PATH.open(encoding="utf-8") as handle:
        cfg = yaml.safe_load(handle)
    df = make_synthetic_series(cfg)
    assert len(df) == cfg["data"]["periods"]
    assert {"Date", "Value", "Moving_Avg", "Value_2"}.issubset(df.columns)


def test_synthetic_series_reproducible() -> None:
    with DEFAULT_CONFIG_PATH.open(encoding="utf-8") as handle:
        cfg = yaml.safe_load(handle)
    a = make_synthetic_series(cfg)
    b = make_synthetic_series(cfg)
    assert a["Value"].tolist() == b["Value"].tolist()
