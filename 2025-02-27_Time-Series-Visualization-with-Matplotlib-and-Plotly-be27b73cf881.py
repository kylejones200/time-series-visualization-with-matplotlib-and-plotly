# Description: Short example for Time Series Visualization with Matplotlib and Plotly.



from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
np.random.seed(42)

time = pd.date_range(start="2023-01-01", periods=100, freq="D")
data = {
    "Date": time,
    "Value": 100 + 2 * np.arange(100) + np.sin(np.linspace(0, 10, 100)) * 10 + np.random.normal(0, 5, 100),
}
df = pd.DataFrame(data)

df["Moving_Avg"] = df["Value"].rolling(window=7).mean()
plt.figure(figsize=(10, 6))
plt.plot(df["Date"], df["Value"], label="Original Data", alpha=0.7)
plt.plot(df["Date"], df["Moving_Avg"], label="7-Day Moving Average", linewidth=2, color="orange")
plt.title("Time Series with Moving Average")
plt.xlabel("Date")
plt.ylabel("Value")
plt.legend()
plt.savefig('moving_average_plot.png')
plt.show()

decomposed = seasonal_decompose(df["Value"], period=30, model="additive")

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
plt.savefig('seasonal_decomposition_plot.png')
plt.show()

df["Day_of_Week"] = df["Date"].dt.day_name()
pivot_table = df.pivot_table(values="Value", index="Day_of_Week", columns=df["Date"].dt.month, aggfunc="mean")
plt.figure(figsize=(10, 6))
sns.heatmap(pivot_table, cmap="coolwarm", annot=True, fmt=".1f")
plt.title("Heatmap of Daily Values")
plt.xlabel("Month")
plt.ylabel("Day of Week")
plt.savefig('heatmap_daily_values.png')
plt.show()

df["Value_2"] = df["Value"] + np.random.normal(0, 10, len(df))
plt.figure(figsize=(10, 8))
plt.subplot(2, 1, 1)
plt.plot(df["Date"], df["Value"], label="Series 1")
plt.title("Time Series 1")
plt.subplot(2, 1, 2)
plt.plot(df["Date"], df["Value_2"], label="Series 2", color="orange")
plt.title("Time Series 2")
plt.tight_layout()
plt.savefig('multiple_time_series_plot.png')
plt.show()

fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Date"], y=df["Value"], mode="lines", name="Value"))
fig.add_annotation(
    x=df["Date"][50],
    y=df["Value"][50],
    text="Notable Point",
    showarrow=True,
    arrowhead=1,
)
fig.update_layout(title="Interactive Line Plot", xaxis_title="Date", yaxis_title="Value")
fig.show()

fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Date"], y=df["Value"], name="Series 1", yaxis="y1"))
fig.add_trace(go.Scatter(x=df["Date"], y=df["Value_2"], name="Series 2", yaxis="y2"))
fig.update_layout(
    title="Dual Axis Plot",
    xaxis={"title": "Date"},
    yaxis={"title": "Series 1", "side": "left"},
    yaxis2={"title": "Series 2", "overlaying": "y", "side": "right"},
)
fig.show()

fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Date"], y=df["Value"], mode="lines", name="Value"))
fig.update_layout(
    title="Time Series with Range Slider",
    xaxis={
        "rangeslider": {"visible": True},
        "type": "date"
    }
)
fig.show()
