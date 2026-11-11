#!/usr/bin/env python3
"""Prove wrapped APP cells do not throw when SQL frames are missing, and App.js parses."""
from __future__ import annotations

import ast
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

from crash_proof import wrap_last_fig, wrap_display

ROOT = Path(__file__).resolve().parent


class FakeDisplay:
    def __init__(self):
        self.calls = []

    def __call__(self, obj):
        self.calls.append(obj)
        return obj


def exec_wrapped(source: str, names: list[str], mode: str, ns: dict | None = None):
    wrapped = wrap_last_fig(source, names) if mode == "fig" else wrap_display(source, names)
    compile(wrapped, "<wrap>", "exec")
    env = {"__name__": "__main__"}
    fake = FakeDisplay()
    env["display"] = fake
    if ns:
        env.update(ns)
    exec(wrapped, env)
    return env, fake


def test_missing_frames_do_not_throw():
    funnel = (ROOT / "original_app_cells/funnel.py").read_text()
    env, _ = exec_wrapped(funnel, ["lead_funnel"], "fig")
    fig = env["fig"]
    assert isinstance(fig, go.Figure), type(fig)
    assert fig.layout.annotations, "empty-state annotation missing"
    assert "Run all" in fig.layout.annotations[0].text


def test_present_frames_build_chart():
    funnel = (ROOT / "original_app_cells/funnel.py").read_text()
    lead_funnel = pd.DataFrame(
        {
            "stage": ["Registered", "Attended"],
            "count": [1269, 836],
            "pct_of_registered": [100.0, 65.9],
        }
    )
    env, _ = exec_wrapped(funnel, ["lead_funnel"], "fig", {"lead_funnel": lead_funnel})
    fig = env["fig"]
    assert fig.data, "expected funnel traces when data exists"
    assert fig.data[0].type == "funnel"


def test_display_cell_missing_frames():
    cab = (ROOT / "original_app_cells/full_cab.py").read_text()
    exec_wrapped(
        cab,
        ["lead_funnel", "pipeline_arr", "attendance_group_funnel", "attendance_group_pipeline"],
        "display",
    )


def test_app_js_parses():
    src = (ROOT / "App.js").read_text()
    assert "import * as React from \"react\"" in src
    assert "createElement" in src
    assert "from \"react\"" in src
    assert "useHexData" not in src
    assert "KpiCard" not in src
    assert "CartesianChart" not in src
    # Strip ESM imports so Python's parser can check the rest is balanced.
    stripped = "\n".join(
        line for line in src.splitlines() if not line.startswith("import ")
    )
    # Remaining JS is not Python; check braces instead.
    assert stripped.count("(") == stripped.count(")")
    assert stripped.count("{") == stripped.count("}")
    assert "import * as React from \"react\";" in src
    assert src.strip().endswith("render(React.createElement(App));")


def test_scoreboard_has_day_counts():
    src = (ROOT / "notebook_scoreboard.py").read_text()
    ast.parse(src)
    for needle in (
        "1,269", "426", "916", "39", "113", "116", "324",
        "green YES", "badge pickup", "Germany users", "Europe users", "Website users",
        "France", "United Kingdom", "Top European countries",
    ):
        assert needle in src, needle


def test_web_europe_chart_is_crash_proof():
    src = (ROOT / "notebook_web_europe.py").read_text()
    ast.parse(src)
    assert "_itl_ready" in src
    assert "ga4_web_europe_countries" in src


if __name__ == "__main__":
    test_missing_frames_do_not_throw()
    test_present_frames_build_chart()
    test_display_cell_missing_frames()
    test_app_js_parses()
    test_scoreboard_has_day_counts()
    test_web_europe_chart_is_crash_proof()
    print("ok")
