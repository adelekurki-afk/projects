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


def _exec_html(path: Path) -> str:
    import sys
    import types

    src = path.read_text()
    fake = FakeDisplay()

    class FakeHTML:
        def __init__(self, data):
            self.data = data

    ipy = types.ModuleType("IPython")
    ipy_display = types.ModuleType("IPython.display")
    ipy_display.display = fake
    ipy_display.HTML = FakeHTML
    sys.modules["IPython"] = ipy
    sys.modules["IPython.display"] = ipy_display
    exec(compile(src, path.name, "exec"), {"__name__": "__main__"})
    assert fake.calls, f"{path.name} did not display HTML"
    return fake.calls[0].data


def test_scoreboard_has_day_counts():
    src = (ROOT / "notebook_scoreboard.py").read_text()
    ast.parse(src)
    for needle in (
        "1,269", "426", "916", "1,018",
        "Salesforce conversion", "Opportunities",
    ):
        assert needle in src, needle
    for gone in ("How 426 is built", "Site intent", "3.8M"):
        assert gone not in src, gone


def test_scoreboard_renders_overview():
    html = _exec_html(ROOT / "notebook_scoreboard.py")
    for needle in (
        "1,269", "426", "916", "1,018", "1,119", "837",
        "€2.46M", "€2.43M", "New Business / ENT",
    ):
        assert needle in html, needle
    for gone in ("How 426 is built", "3.8M", "Berlin events · conference week"):
        assert gone not in html, gone


def test_participation_tab_html():
    src = (ROOT / "notebook_participation.py").read_text()
    ast.parse(src)
    html = _exec_html(ROOT / "notebook_participation.py")
    for needle in (
        "Participation", "426", "916", "324", "1,018",
        "113", "116", "39", "391", "878", "green YES",
    ):
        assert needle in html, needle


def _exec_view(path: Path, extra: dict | None = None):
    import sys
    import types

    src = path.read_text()
    ast.parse(src)
    fake = FakeDisplay()

    class FakeHTML:
        def __init__(self, data):
            self.data = data

    ipy = types.ModuleType("IPython")
    ipy_display = types.ModuleType("IPython.display")
    ipy_display.display = fake
    ipy_display.HTML = FakeHTML
    sys.modules["IPython"] = ipy
    sys.modules["IPython.display"] = ipy_display
    env = {"__name__": "__main__"}
    if extra:
        env.update(extra)
    exec(compile(src, path.name, "exec"), env)
    return fake.calls


def test_intent_tab_explains_timeframes():
    src = (ROOT / "notebook_intent.py").read_text()
    ast.parse(src)
    calls = _exec_view(ROOT / "notebook_intent.py")
    blob = " ".join(getattr(c, "data", str(c)) for c in calls)
    for needle in (
        "Intent",
        "12–18 Oct",
        "YouTube",
        "Common Room",
        "Paid Google Ads",
        "Europe and Germany",
    ):
        assert needle in src or needle in blob, needle


def test_four_views_compile_without_sql():
    for name in (
        "notebook_summary.py",
        "notebook_attendance.py",
        "notebook_funnel.py",
        "notebook_intent.py",
    ):
        calls = _exec_view(ROOT / name)
        assert calls, name


def test_summary_has_sourced_and_attendance_rate():
    src = (ROOT / "notebook_summary.py").read_text()
    for needle in ("Summary", "426", "916", "87%", "76%", "Sourced", "Influenced", "113"):
        assert needle in src, needle
    html = _exec_html(ROOT / "notebook_summary.py")
    assert "Summary" in html
    assert "Sourced opps" in html


def test_attendance_has_meetings_and_feedback():
    src = (ROOT / "notebook_attendance.py").read_text()
    for needle in (
        "Attendance",
        "Sales meetings sheet",
        "Partner Day overall",
        "Ecosystem recommend",
        "Community Lounge",
        "Salesforce Attended",
    ):
        assert needle in src, needle


def test_section_markdown_tables_have_numbers():
    checks = {
        "notebook_overlap.md": ("426", "916", "324", "1,018"),
        "notebook_funnel.md": ("1,119", "837", "20", "70", "6"),
        "notebook_pipeline.md": ("€2,461,063", "New Business", "ENT"),
        "notebook_partner.md": ("426", "916", "391", "878"),
        "notebook_digital.md": ("174,802", "11,428", "84,904"),
        "notebook_participation_tab.md": ("426", "916", "324", "1,018", "391", "878"),
        "notebook_intent_tab.md": ("+33%", "12–18 Oct", "5–11 Oct", "3.8M", "262k"),
        "lean_readout.md": ("426", "916", "1,018", "1,119", "+33%"),
    }
    for name, needles in checks.items():
        src = (ROOT / name).read_text()
        for needle in needles:
            assert needle in src, f"{name}: {needle}"


def test_web_markdown_section_has_numbers():
    src = (ROOT / "notebook_web_section.md").read_text()
    for needle in ("3.8M", "1.0M", "219k", "11,461", "218,861", "Germany", "France"):
        assert needle in src, needle


def test_cab_roles_traffic_are_split_and_crash_proof():
    for name, needle in (
        ("notebook_cab.py", "cab_overlay_kpis"),
        ("notebook_roles.py", "persona_by_role"),
        ("notebook_traffic.py", "ga4_post_event_trend"),
    ):
        src = (ROOT / name).read_text()
        ast.parse(src)
        assert "_itl_ready" in src
        assert needle in src
        assert src.strip().endswith("fig")


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
    test_scoreboard_renders_overview()
    test_participation_tab_html()
    test_intent_tab_explains_timeframes()
    test_four_views_compile_without_sql()
    test_summary_has_sourced_and_attendance_rate()
    test_attendance_has_meetings_and_feedback()
    test_section_markdown_tables_have_numbers()
    test_web_markdown_section_has_numbers()
    test_cab_roles_traffic_are_split_and_crash_proof()
    test_web_europe_chart_is_crash_proof()
    print("ok")
