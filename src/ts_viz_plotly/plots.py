from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose


def _save_or_show(path: Path | None, *, dpi: int, show: bool) -> None:
    if path is not None:
        path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(path, dpi=dpi, bbox_inches="tight")
    if show:
        plt.show()
    plt.close()


def plot_moving_average(
    df: pd.DataFrame,
    *,
    path: Path | None,
    dpi: int,
    show: bool,
) -> None:
    plt.figure(figsize=(10, 6))
    plt.plot(df["Date"], df["Value"], label="Original Data", alpha=0.7)
    plt.plot(
        df["Date"],
        df["Moving_Avg"],
        label="7-Day Moving Average",
        linewidth=2,
        color="orange",
    )
    plt.title("Time Series with Moving Average")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    _save_or_show(path, dpi=dpi, show=show)


def plot_seasonal_decomposition(
    df: pd.DataFrame,
    *,
    period: int,
    path: Path | None,
    dpi: int,
    show: bool,
) -> None:
    decomposed = seasonal_decompose(df["Value"], period=period, model="additive")
    plt.figure(figsize=(10, 8))
    plt.subplot(311)
    plt.plot(df["Date"], decomposed.trend, label="Trend", color="blue")
    plt.title("Trend Component")
    plt.subplot(312)
    plt.plot(df["Date"], decomposed.seasonal, label="Seasonality", color="green")
    plt.title("Seasonal Component")
    plt.subplot(313)
    plt.plot(df["Date"], decomposed.resid, label="Residual", color="red")
    plt.title("Residual Component")
    plt.tight_layout()
    _save_or_show(path, dpi=dpi, show=show)


def plot_day_of_week_heatmap(
    df: pd.DataFrame,
    *,
    path: Path | None,
    dpi: int,
    show: bool,
) -> None:
    pivot_table = df.pivot_table(
        values="Value",
        index="Day_of_Week",
        columns=df["Date"].dt.month,
        aggfunc="mean",
    )
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_table, cmap="coolwarm", annot=True, fmt=".1f")
    plt.title("Heatmap of Daily Values")
    plt.xlabel("Month")
    plt.ylabel("Day of Week")
    _save_or_show(path, dpi=dpi, show=show)


def plot_multiple_series(
    df: pd.DataFrame,
    *,
    path: Path | None,
    dpi: int,
    show: bool,
) -> None:
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    plt.plot(df["Date"], df["Value"], label="Series 1")
    plt.title("Time Series 1")
    plt.subplot(2, 1, 2)
    plt.plot(df["Date"], df["Value_2"], label="Series 2", color="orange")
    plt.title("Time Series 2")
    plt.tight_layout()
    _save_or_show(path, dpi=dpi, show=show)


def _write_plotly(fig: go.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(path, include_plotlyjs="cdn")


def plot_plotly_annotated(df: pd.DataFrame, path: Path) -> None:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Value"], mode="lines", name="Value"))
    fig.add_annotation(
        x=df["Date"].iloc[50],
        y=df["Value"].iloc[50],
        text="Notable Point",
        showarrow=True,
        arrowhead=1,
    )
    fig.update_layout(
        title="Interactive Line Plot",
        xaxis_title="Date",
        yaxis_title="Value",
    )
    _write_plotly(fig, path)


def plot_plotly_dual_axis(df: pd.DataFrame, path: Path) -> None:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Value"], name="Series 1", yaxis="y1"))
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Value_2"], name="Series 2", yaxis="y2"))
    fig.update_layout(
        title="Dual Axis Plot",
        xaxis={"title": "Date"},
        yaxis={"title": "Series 1", "side": "left"},
        yaxis2={"title": "Series 2", "overlaying": "y", "side": "right"},
    )
    _write_plotly(fig, path)


def plot_plotly_range_slider(df: pd.DataFrame, path: Path) -> None:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Value"], mode="lines", name="Value"))
    fig.update_layout(
        title="Time Series with Range Slider",
        xaxis={"rangeslider": {"visible": True}, "type": "date"},
    )
    _write_plotly(fig, path)


def run_all_plots(df: pd.DataFrame, cfg: dict[str, Any]) -> dict[str, Path]:
    """Generate Matplotlib PNGs and Plotly HTML files; return output paths."""
    out_cfg = cfg.get("output") or {}
    data_cfg = cfg.get("data") or {}
    figures_dir = Path(out_cfg.get("figures_dir", "outputs/figures"))
    plotly_dir = Path(out_cfg.get("plotly_dir", "outputs/plotly"))
    fmt = str(out_cfg.get("figure_format", "png"))
    dpi = int(out_cfg.get("figure_dpi", 120))
    show = bool(out_cfg.get("show", False))
    period = int(data_cfg.get("decomposition_period", 30))
    if not figures_dir.is_absolute():
        from ts_viz_plotly.paths import resolve_project_path

        figures_dir = resolve_project_path(figures_dir)
        plotly_dir = resolve_project_path(plotly_dir)

    figures: dict[str, Path] = {}
    static_specs = [
        ("moving_average", plot_moving_average),
        ("seasonal_decomposition", plot_seasonal_decomposition),
        ("day_of_week_heatmap", plot_day_of_week_heatmap),
        ("multiple_series", plot_multiple_series),
    ]
    for name, func in static_specs:
        out_path = figures_dir / f"{name}.{fmt}"
        if name == "seasonal_decomposition":
            func(df, period=period, path=out_path, dpi=dpi, show=show)  # type: ignore[operator]
        else:
            func(df, path=out_path, dpi=dpi, show=show)  # type: ignore[operator]
        figures[name] = out_path

    plotly_specs = [
        ("interactive_annotated", plot_plotly_annotated),
        ("dual_axis", plot_plotly_dual_axis),
        ("range_slider", plot_plotly_range_slider),
    ]
    for name, func in plotly_specs:
        out_path = plotly_dir / f"{name}.html"
        func(df, out_path)
        figures[name] = out_path

    return figures
