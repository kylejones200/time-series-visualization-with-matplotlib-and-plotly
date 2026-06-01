# Time Series Visualization with Matplotlib and Plotly

Published: 2025-02-27  
Medium: [Time Series Visualization with Matplotlib and Plotly](https://medium.com/@kyle-t-jones/time-series-visualization-with-matplotlib-and-plotly-be27b73cf881)

Matplotlib and Plotly examples for moving averages, seasonal decomposition, heatmaps, and interactive charts. Companion code for the article (`article.md`).

## Business context

Visualizing time series data reveals patterns, trends, seasonality, and anomalies that are not immediately visible in raw data. Basic line plots offer a starting point, but advanced visualizations provide deeper insights. This chapter explores intermediate techniques for time series visualization using Matplotlib and Plotly. It focuses on interactive features, customizations, and specialized plots that highlight complex patterns and relationships in the data.

Advanced visualizations show seasonality, trends, and periodicity more clearly. They also allow comparisons between multiple time series or features on a single view. Plotly adds interactivity, making data exploration more dynamic and engaging. These visualizations simplify complex data stories, allowing executives and stakeholders to understand key insights quickly.

Matplotlib is the most widely used visualization library in Python. It provides powerful tools for creating detailed and publication-quality graphs. In this section, we use a sample time series dataset to demonstrate various visualization techniques beyond basic line graphs.

## Quick start

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run ts-viz-run
```

Outputs:

| Path | Contents |
|------|----------|
| `outputs/figures/` | Matplotlib PNGs (moving average, decomposition, heatmap, dual panel) |
| `outputs/plotly/` | Interactive Plotly HTML files |
| `outputs/results.json` | Run metadata and relative figure paths |

## Project layout

```
config.yaml              # synthetic data and output settings
config.local.yaml.example
pyproject.toml / uv.lock
src/ts_viz_plotly/       # data generation, plotting, CLI
outputs/figures/         # generated PNGs (gitignored except .gitkeep)
outputs/plotly/          # generated HTML (gitignored except .gitkeep)
tests/
article.md
2025-02-27_*.py          # original Medium export (delegates to package)
```

## Configuration

Edit `config.yaml`:

- `data.seed`, `data.periods` — synthetic series length and reproducibility
- `data.moving_average_window` — rolling mean window (default 7)
- `data.decomposition_period` — seasonal decomposition period (default 30)
- `output.show` — set `true` to open interactive windows locally

Machine-specific overrides: copy `config.local.yaml.example` to `config.local.yaml` (gitignored).

## Development

```bash
uv sync --extra dev
uv run pytest
uv run ruff check src tests
```

CI runs ruff and pytest on push/PR (see `.github/workflows/ci.yml`).

## Disclaimer

Educational/demo code only. Not financial, safety, or engineering advice. Use at your own risk. Verify results independently before any production or operational use.

## License

MIT — see [LICENSE](LICENSE).