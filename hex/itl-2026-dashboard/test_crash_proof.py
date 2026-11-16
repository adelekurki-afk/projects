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


def _blob(calls) -> str:
    parts = []
    for c in calls:
        data = getattr(c, "data", None)
        if isinstance(data, str):
            parts.append(data)
        elif isinstance(c, pd.DataFrame):
            parts.append(c.to_csv(index=False))
        elif isinstance(c, go.Figure):
            title = c.layout.title.text if c.layout.title else ""
            parts.append(str(title or ""))
            for tr in c.data:
                for attr in ("text", "x", "y", "value", "name", "title"):
                    val = getattr(tr, attr, None)
                    if val is not None:
                        parts.append(str(val))
                if getattr(tr, "type", None) == "table":
                    header = getattr(tr, "header", None)
                    cells = getattr(tr, "cells", None)
                    if header is not None:
                        parts.append(str(getattr(header, "values", "")))
                        fill = getattr(header, "fill", None)
                        if fill is not None:
                            parts.append(str(getattr(fill, "color", "")))
                    if cells is not None:
                        parts.append(str(getattr(cells, "values", "")))
                        fill = getattr(cells, "fill", None)
                        if fill is not None:
                            parts.append(str(getattr(fill, "color", "")))
        else:
            parts.append(str(c))
    return "\n".join(parts)


def test_scoreboard_has_day_counts():
    src = (ROOT / "notebook_scoreboard.py").read_text()
    ast.parse(src)
    for needle in (
        "1,269", "426", "916", "1,018",
        "Opportunities",
    ):
        assert needle in src, needle
    for gone in ("How 426 is built", "Site intent", "3.8M"):
        assert gone not in src, gone


def test_scoreboard_renders_overview():
    calls = _exec_view(ROOT / "notebook_scoreboard.py")
    blob = _blob(calls)
    for needle in (
        "1,269", "426", "916", "1,018", "1,119", "837",
        "€2.46M", "€2.43M", "New Business / ENT",
    ):
        assert needle in blob, needle
    for gone in ("How 426 is built", "3.8M", "Berlin events · conference week"):
        assert gone not in blob, gone
    assert any(isinstance(c, go.Figure) for c in calls)
    tables = [
        c
        for c in calls
        if isinstance(c, go.Figure) and c.data and getattr(c.data[0], "type", None) == "table"
    ]
    assert tables
    assert "#87003C" in str(tables[0].data[0].header.fill.color)


def test_participation_tab_html():
    src = (ROOT / "notebook_participation.py").read_text()
    ast.parse(src)
    blob = src + "\n" + _blob(_exec_view(ROOT / "notebook_participation.py"))
    for needle in (
        "Participation", "426", "916", "324", "1,018",
        "113", "116", "39", "391", "878", "green YES",
    ):
        assert needle in blob, needle


def test_one_figure_chart_library():
    for path in sorted((ROOT / "charts").glob("*.py")):
        calls = _exec_view(path)
        figs = [c for c in calls if isinstance(c, go.Figure)]
        assert figs, path.name
        assert path.read_text().count("\ndisplay(") == 1, path.name
        kinds = {getattr(tr, "type", None) for fig in figs for tr in fig.data}
        assert kinds & {"bar", "scatter", "funnel", "indicator", "table"}, (path.name, kinds)


def test_sfdc_charts_are_separate_visuals():
    contact = _exec_view(ROOT / "charts/sfdc_lead_contact.py")
    segment = _exec_view(ROOT / "charts/sfdc_segment.py")
    region = _exec_view(ROOT / "charts/sfdc_region.py")
    partner = _exec_view(ROOT / "charts/partner_vs_eco.py")
    contact_fig = next(c for c in contact if isinstance(c, go.Figure))
    segment_fig = next(c for c in segment if isinstance(c, go.Figure))
    region_fig = next(c for c in region if isinstance(c, go.Figure))
    partner_fig = next(c for c in partner if isinstance(c, go.Figure))
    assert [t.name for t in contact_fig.data] == ["Lead", "Contact"]
    assert "ENT" in [t.name for t in segment_fig.data]
    assert "DACH" not in [t.name for t in segment_fig.data]
    assert "DACH" in [t.name for t in region_fig.data]
    assert "ENT" not in [t.name for t in region_fig.data]
    assert {t.name for t in partner_fig.data} == {"Partner Day", "Ecosystem Day"}
    assert "TICKET" not in (ROOT / "charts/partner_vs_eco.py").read_text()
    assert "sales segment and region" not in (ROOT / "charts/sfdc_segment.py").read_text()
    assert "sales segment and region" not in (ROOT / "charts/sfdc_region.py").read_text()


def test_participation_segment_and_country_are_separate():
    partner_seg = next(c for c in _exec_view(ROOT / "charts/partner_segment.py") if isinstance(c, go.Figure))
    eco_seg = next(c for c in _exec_view(ROOT / "charts/eco_segment.py") if isinstance(c, go.Figure))
    cab_seg = next(c for c in _exec_view(ROOT / "charts/cab_segment.py") if isinstance(c, go.Figure))
    partner_cty = next(c for c in _exec_view(ROOT / "charts/partner_country.py") if isinstance(c, go.Figure))
    eco_cty = next(c for c in _exec_view(ROOT / "charts/eco_country.py") if isinstance(c, go.Figure))
    cab_cty = next(c for c in _exec_view(ROOT / "charts/cab_country.py") if isinstance(c, go.Figure))
    assert list(partner_seg.data[0].y) == ["Unknown", "SMB", "MM", "ENT"]
    assert "Germany" not in list(partner_seg.data[0].y)
    assert "ENT" not in list(partner_cty.data[0].y)
    assert "Germany" in list(partner_cty.data[0].y)
    assert "Partner Day" in str(partner_seg.layout.title.text)
    assert "Ecosystem Day" in str(eco_seg.layout.title.text)
    assert str(cab_seg.layout.title.text).startswith("CAB")
    assert int(eco_seg.data[0].x[-1]) == 180
    assert int(cab_seg.data[0].x[-1]) == 28
    assert int(eco_cty.data[0].x[-1]) == 542
    assert int(cab_cty.data[0].x[-1]) == 20
    sql = (ROOT / "lean/attendance_segment_country.sql").read_text()
    assert "701cj00001LbE7XAAV" in sql
    assert "701cj00001LbEQvAAN" in sql
    assert "market_segment" in sql
    assert "country" in sql


def test_ticket_sales_are_charts():
    daily_calls = _exec_view(ROOT / "notebook_ticket_daily.py")
    mix_calls = _exec_view(ROOT / "notebook_ticket_mix.py")
    table_calls = _exec_view(ROOT / "notebook_ticket_table.py")
    daily_fig = next(c for c in daily_calls if isinstance(c, go.Figure))
    mix_fig = next(c for c in mix_calls if isinstance(c, go.Figure))
    table_fig = next(c for c in table_calls if isinstance(c, go.Figure))
    assert daily_fig.data[0].type == "bar"
    assert any(getattr(tr, "yaxis", None) == "y2" for tr in daily_fig.data)
    assert any(getattr(tr, "stackgroup", None) == "tickets" for tr in mix_fig.data)
    assert table_fig.data[0].type == "table"
    assert "#87003C" in str(table_fig.data[0].header.fill.color)
    blob = _blob(table_calls)
    assert "1,043" in blob or "1043" in blob
    bundled = _exec_ns(ROOT / "notebook_tickets.py")
    assert int(bundled["ticket_sales_daily"].iloc[-1]["unique_people"]) == 1043
    assert int(bundled["ticket_sales_daily"].iloc[-1]["registrations"]) == 1151
    sql = (ROOT / "lean/ticket_sales.sql").read_text()
    assert "FROM UNNEST" in sql
    assert "pace_to_850" in sql
    assert "2026-10-10" in sql


def _prep_exec(path: Path, extra: dict | None = None):
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
    ipy_display.Markdown = FakeHTML
    sys.modules["IPython"] = ipy
    sys.modules["IPython.display"] = ipy_display
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    env = {"__name__": "__main__"}
    if extra:
        env.update(extra)
    exec(compile(src, path.name, "exec"), env)
    return env, fake


def _exec_view(path: Path, extra: dict | None = None):
    _, fake = _prep_exec(path, extra)
    return fake.calls


def _exec_ns(path: Path, extra: dict | None = None):
    env, _ = _prep_exec(path, extra)
    return env


def test_intent_tab_explains_timeframes():
    src = (ROOT / "notebook_intent.py").read_text()
    ast.parse(src)
    calls = _exec_view(ROOT / "notebook_intent.py")
    blob = _blob(calls)
    for needle in (
        "Intent",
        "12–18 Oct",
        "YouTube",
        "Paid Google Ads",
        "n8n.io users · Europe",
        "n8n.io users · Germany",
        "n8n.io users · worldwide",
    ):
        assert needle in src or needle in blob, needle
    assert "Common Room" not in src
    assert "Common Room" not in blob
    titles = [str(c.layout.title.text) for c in calls if isinstance(c, go.Figure)]
    assert "n8n.io users · worldwide" in titles
    assert "n8n.io users · Europe" in titles
    assert "n8n.io users · Germany" in titles
    assert not any("Europe and Germany" in t for t in titles)
    europe_fig = next(c for c in _exec_view(ROOT / "charts/users_europe.py") if isinstance(c, go.Figure))
    germany_fig = next(c for c in _exec_view(ROOT / "charts/users_germany.py") if isinstance(c, go.Figure))
    assert "Europe" in str(europe_fig.layout.title.text)
    assert "Germany" not in str(europe_fig.layout.title.text)
    assert "Germany" in str(germany_fig.layout.title.text)
    assert "Europe" not in str(germany_fig.layout.title.text)
    assert europe_fig.data[0].type == "scatter"
    assert germany_fig.data[0].type == "scatter"


def test_four_views_compile_without_sql():
    for name in (
        "notebook_summary.py",
        "notebook_attendance.py",
        "notebook_funnel.py",
        "notebook_intent.py",
        "notebook_survey_eco.py",
        "notebook_survey_partner.py",
        "notebook_survey_session.py",
        "notebook_sfdc_lead_progression.py",
        "notebook_sfdc_lead_reached.py",
    ):
        calls = _exec_view(ROOT / name)
        assert calls, name
    funnel_calls = _exec_view(ROOT / "notebook_funnel.py")
    funnel_blob = _blob(funnel_calls)
    assert "SFDC lead reached" in funnel_blob
    assert "sales segment" in funnel_blob
    assert "region" in funnel_blob
    assert "1,102" in funnel_blob or "1102" in funnel_blob or "441" in funnel_blob
    funnel_figs = [c for c in funnel_calls if isinstance(c, go.Figure)]
    assert funnel_figs, "Funnel Chart should open with a visual"
    first = funnel_figs[0]
    assert first.data[0].type == "funnel"
    assert "Event people" in str(first.layout.title.text)
    seg = next(
        c
        for c in funnel_figs
        if c.data and getattr(c.data[0], "type", None) == "bar" and "ENT" in [t.name for t in c.data]
    )
    assert seg.data[0].orientation == "h"
    assert "DACH" not in [t.name for t in seg.data]
    reg = next(
        c
        for c in funnel_figs
        if c.data and getattr(c.data[0], "type", None) == "bar" and "DACH" in [t.name for t in c.data]
    )
    assert "ENT" not in [t.name for t in reg.data]
    titles = [str(c.layout.title.text) for c in funnel_figs]
    assert any([t.name for t in c.data] == ["Lead", "Contact"] for c in funnel_figs)
    assert any("sales segment" in t for t in titles)
    assert any("region" in t for t in titles)
    assert not any("sales segment and region" in t for t in titles)
    assert not any("Lead progression" in t for t in titles)
    tables = [
        c
        for c in funnel_figs
        if c.data and getattr(c.data[0], "type", None) == "table"
    ]
    headers = "\n".join(str(t.data[0].header.values) for t in tables)
    assert "ENT" in headers
    assert "DACH" in headers


def test_summary_has_sourced_and_attendance_rate():
    src = (ROOT / "notebook_summary.py").read_text()
    for needle in ("426", "916", "87%", "76%", "Sourced", "Influenced", "113"):
        assert needle in src, needle
    blob = src + "\n" + _blob(_exec_view(ROOT / "notebook_summary.py"))
    assert "Sourced opps" in blob
    assert "Participants per day" in blob


def test_survey_and_lead_cells_have_pin_labels():
    eco = _blob(_exec_view(ROOT / "notebook_survey_eco.py"))
    partner = _blob(_exec_view(ROOT / "notebook_survey_partner.py"))
    session = _blob(_exec_view(ROOT / "notebook_survey_session.py"))
    for needle in ("Recommend attending In The Loop", "9.1", "NPS", "n8n Agents"):
        assert needle in eco or needle in (ROOT / "notebook_survey_eco.py").read_text(), needle
    assert "9.1" in (ROOT / "notebook_survey_eco.py").read_text()
    assert "n=20" in partner or "n=20" in (ROOT / "notebook_survey_partner.py").read_text()
    assert "Session score" in session or "Session /5" in (ROOT / "notebook_survey_session.py").read_text()
    for path in (
        "lean/lead_campaign_statuses.sql",
        "lean/lead_sfdc_statuses.sql",
        "lean/lead_progression.sql",
        "lean/lead_sfdc_reached.sql",
        "lean/lead_sfdc_reached_dims.sql",
    ):
        src = (ROOT / path).read_text()
        assert "701cj0000157ynMAAQ" in src
    assert "LeadHistory" in (ROOT / "lean/lead_progression.sql").read_text()
    assert "fct_campaign_member_pipeline" in (ROOT / "lean/lead_sfdc_statuses.sql").read_text()
    reached_sql = (ROOT / "lean/lead_sfdc_reached.sql").read_text()
    assert "as_lead" in reached_sql
    assert "as_contact" in reached_sql
    assert "ContactHistory" in reached_sql
    assert "ENT" in reached_sql
    assert "DACH" in reached_sql
    assert "market_segment" in reached_sql
    dim_sql = (ROOT / "lean/lead_sfdc_reached_dims.sql").read_text()
    assert "market_segment" in dim_sql
    assert "sub_region" in dim_sql
    blob = _blob(_exec_view(ROOT / "notebook_sfdc_lead_progression.py"))
    assert "sales segment" in blob
    assert "region" in blob
    assert "441" in blob
    assert "DACH" in blob
    reached_blob = _blob(_exec_view(ROOT / "notebook_sfdc_lead_reached.py"))
    assert "SFDC lead reached" in reached_blob
    assert "Contact" in reached_blob
    assert "546" in reached_blob
    assert "206" in reached_blob


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
        "notebook_funnel.md": ("1,102", "314", "Working", "Qualified", "1,119", "837", "20", "70", "6"),
        "notebook_pipeline.md": ("€2,461,063", "New Business", "ENT"),
        "notebook_partner.md": ("426", "916", "391", "878"),
        "notebook_digital.md": ("174,802", "11,428", "84,904"),
        "notebook_overview.md": ("426", "916", "1,018", "1,119", "€2.46M"),
        "notebook_participation_tab.md": ("426", "916", "324", "1,018", "391", "878"),
        "notebook_registration.md": ("1,151", "1,043", "850", "652", "123%", "chart icon"),
        "tables/section_outline.md": ("Tables", "Outline"),
        "tables/section_registration.md": ("Registration", "chart icon"),
        "tables/section_funnel.md": ("Funnel", "restyle"),
        "notebook_intent_tab.md": ("+33%", "12–18 Oct", "5–11 Oct", "3.8M", "262k"),
        "lean_readout.md": ("426", "916", "1,018", "1,119", "+33%"),
        "notebook_survey_eco.md": ("9.1", "NPS", "43", "33 promoters"),
        "notebook_survey_partner.md": ("9.1", "n=20", "Solution", "8.5"),
        "notebook_survey_session.md": ("4.8", "66", "24", "36"),
        "notebook_lead_tables.md": ("1,102", "314", "Working", "Qualified", "Funnel Chart"),
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


def test_native_section_tables_are_dataframes():
    expected = {
        "tables/visits.py": ("visits", 8, "people"),
        "tables/pipeline_summary.py": ("pipeline_summary", 3, "amount_eur"),
        "tables/opps_by_segment.py": ("opportunities_by_segment", 4, "total_eur"),
        "tables/role_mix.py": ("role_mix", 12, "partner_day"),
        "tables/also_on_site.py": ("also_on_site", 10, "value"),
        "tables/staff_by_crew.py": ("staff_by_crew", 5, "registered"),
        "tables/speakers_by_day.py": ("speakers_by_day", 2, "speakers"),
        "tables/paid_search.py": ("paid_search_terms", 15, "impressions"),
        "tables/eco_parts.py": ("eco_programme_parts", 8, "mean_5"),
        "tables/eco_ops.py": ("eco_operations", 6, "mean_5"),
        "tables/eco_who.py": ("eco_who_answered", 8, "n"),
        "tables/partner_tracks.py": ("partner_tracks", 3, "attended"),
        "tables/session_ratings.py": ("session_ratings", 12, "session_mean"),
        "tables/attribution_kpis.py": ("attribution_kpis", 3, "amount_eur"),
        "tables/sfdc_lead_reached.py": ("sfdc_lead_reached_table", 6, "people_ever_reached"),
        "tables/event_people.py": ("event_people_funnel_table", 5, "people"),
        "tables/weekly_users.py": ("weekly_n8n_users", 23, "n8n_users"),
        "tables/youtube_views.py": ("youtube_views", 18, "views_gained"),
        "tables/attendance_region.py": ("attendance_region", 6, "partner_day"),
    }
    for name, (var, rows, col) in expected.items():
        env = _exec_ns(ROOT / name)
        frame = env[var]
        assert isinstance(frame, pd.DataFrame), name
        assert len(frame) == rows, name
        assert col in frame.columns, name
        leftover = env.get("display")
        if leftover is not None and getattr(leftover, "calls", None):
            figs = [c for c in leftover.calls if isinstance(c, go.Figure)]
            assert not figs, f"{name} still builds a Plotly figure"


def test_app_tables_use_n8n_pink():
    for name in (
        "notebook_scoreboard.py",
        "notebook_funnel.py",
        "notebook_participation.py",
        "notebook_attendance.py",
        "notebook_intent.py",
        "notebook_survey_eco.py",
        "notebook_survey_partner.py",
        "notebook_survey_session.py",
        "notebook_sfdc_lead_progression.py",
        "notebook_sfdc_lead_reached.py",
        "notebook_summary.py",
        "notebook_staff_speakers.py",
    ):
        calls = _exec_view(ROOT / name)
        tables = [
            c
            for c in calls
            if isinstance(c, go.Figure) and c.data and getattr(c.data[0], "type", None) == "table"
        ]
        assert tables, name
        for fig in tables:
            fill = str(fig.data[0].header.fill.color)
            assert "#87003C" in fill, f"{name} header {fill}"
            cells = str(fig.data[0].cells.fill.color)
            assert "#FFBCCA" in cells, f"{name} cells {cells}"
        leftover = [c for c in calls if isinstance(c, pd.DataFrame)]
        assert not leftover, f"{name} still displays a pandas table"


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
    test_one_figure_chart_library()
    test_sfdc_charts_are_separate_visuals()
    test_participation_segment_and_country_are_separate()
    test_ticket_sales_are_charts()
    test_native_section_tables_are_dataframes()
    test_intent_tab_explains_timeframes()
    test_four_views_compile_without_sql()
    test_survey_and_lead_cells_have_pin_labels()
    test_summary_has_sourced_and_attendance_rate()
    test_attendance_has_meetings_and_feedback()
    test_section_markdown_tables_have_numbers()
    test_web_markdown_section_has_numbers()
    test_cab_roles_traffic_are_split_and_crash_proof()
    test_web_europe_chart_is_crash_proof()
    test_app_tables_use_n8n_pink()
    print("ok")
