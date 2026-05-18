from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any

from ts_viz_plotly import __version__
from ts_viz_plotly.config import configure_logging, load_config
from ts_viz_plotly.data import make_synthetic_series
from ts_viz_plotly.paths import DEFAULT_CONFIG_PATH, path_relative_to_project, resolve_project_path
from ts_viz_plotly.plots import run_all_plots

logger = logging.getLogger(__name__)


def run(config_path: Path | str | None = None) -> dict[str, Any]:
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    cfg = load_config(path)
    configure_logging(cfg)
    df = make_synthetic_series(cfg)
    figures = run_all_plots(df, cfg)
    out_cfg = cfg.get("output") or {}
    results_path = resolve_project_path(out_cfg.get("results_path", "outputs/results.json"))
    results_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": __version__,
        "rows": len(df),
        "date_range": {
            "start": df["Date"].iloc[0].isoformat(),
            "end": df["Date"].iloc[-1].isoformat(),
        },
        "figures": {k: path_relative_to_project(v) for k, v in figures.items()},
    }
    results_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    logger.info("Wrote %s (%d figures)", results_path, len(figures))
    return {"df": df, "figures": figures, "results_path": results_path}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Time series visualization with Matplotlib and Plotly"
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="Path to config.yaml",
    )
    args = parser.parse_args()
    run(args.config)


if __name__ == "__main__":
    main()
