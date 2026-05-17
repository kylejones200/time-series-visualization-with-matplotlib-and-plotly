from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
import yaml

from ts_viz_plotly.paths import DEFAULT_CONFIG_PATH
from ts_viz_plotly.runner import run


@pytest.fixture
def headless_config(tmp_path: Path) -> Path:
    with DEFAULT_CONFIG_PATH.open(encoding="utf-8") as handle:
        cfg = yaml.safe_load(handle)
    cfg["output"]["figures_dir"] = str(tmp_path / "figures")
    cfg["output"]["plotly_dir"] = str(tmp_path / "plotly")
    cfg["output"]["results_path"] = str(tmp_path / "results.json")
    cfg["output"]["figure_dpi"] = 72
    cfg["output"]["show"] = False
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    return path


def test_run_pipeline_writes_outputs(headless_config: Path) -> None:
    os.environ.setdefault("MPLBACKEND", "Agg")
    result = run(headless_config)
    results_path = result["results_path"]
    assert results_path.is_file()

    payload = json.loads(results_path.read_text(encoding="utf-8"))
    assert payload["rows"] == 100
    assert len(payload["figures"]) == 7

    for fig_path in result["figures"].values():
        assert fig_path.is_file()
        assert fig_path.stat().st_size > 0
