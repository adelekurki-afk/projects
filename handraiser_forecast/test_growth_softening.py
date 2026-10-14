"""The softening steps are easy to get wrong at the boundaries, so each one is pinned."""

from pathlib import Path

import pandas as pd
import pytest

from growth_softening import (
    CONFIG,
    backtest,
    clamp_growth,
    damped_growth,
    prepare_forecast,
    shrinkage_weight,
    shrunk_growth,
)


def test_shrinkage_weight_is_half_when_volume_equals_k():
    assert shrinkage_weight(100, 100) == 0.5


def test_shrinkage_weight_ignores_a_segment_with_no_volume():
    assert shrinkage_weight(0, 50) == 0.0


def test_shrunk_growth_blends_segment_rate_toward_the_total():
    # A segment of size k is only half trusted, so its rate moves halfway to the total.
    assert shrunk_growth(0.40, 0.10, n=100, k=100) == pytest.approx(0.25)


def test_damping_pulls_toward_the_anchor_by_phi_to_the_horizon():
    # Quarter 1 keeps 75% of the gap. Quarter 2 keeps 75% of what quarter 1 kept.
    assert damped_growth(anchor=0.0, g_shrunk=-0.40, phi=0.75, horizon=1) == pytest.approx(-0.30)
    assert damped_growth(anchor=0.0, g_shrunk=-0.40, phi=0.75, horizon=2) == pytest.approx(-0.225)


def test_clamp_limits_the_rate_and_flags_only_when_it_binds():
    capped, capped_flag = clamp_growth(0.40, floor=-0.20, cap=0.25)
    floored, floored_flag = clamp_growth(-0.50, floor=-0.20, cap=0.25)
    inside, inside_flag = clamp_growth(-0.10, floor=-0.20, cap=0.25)
    assert capped == pytest.approx(0.25)
    assert capped_flag is True
    assert floored == pytest.approx(-0.20)
    assert floored_flag is True
    assert inside == pytest.approx(-0.10)
    assert inside_flag is False


def test_anchor_is_zero_until_eight_trailing_yoy_rates_exist():
    # Seven quarters cannot form a trailing-twelve-month rate from a year earlier.
    quarterly = _panel(quarters=7, segment_leads={"A": 10, "B": 30})
    forecast = prepare_forecast(quarterly, CONFIG)
    assert set(forecast["anchor"]) == {0.0}
    # The quarter a year after the missing quarter has no base, so the count stays blank.
    missing_base = forecast[forecast["forecast_quarter"] == "2026-Q4"]
    assert missing_base["forecast_handraisers"].isna().all()


def test_segment_forecasts_sum_to_the_total_row():
    quarterly = _panel(quarters=12, segment_leads={"A": 10, "B": 30})
    forecast = prepare_forecast(quarterly, CONFIG)
    segments = forecast[forecast["segment"] != "All segments"]
    totals = forecast[forecast["segment"] == "All segments"]
    summed = (
        segments.groupby(["region", "scenario", "forecast_quarter"], as_index=False)["forecast_handraisers"]
        .sum()
        .rename(columns={"forecast_handraisers": "summed"})
    )
    merged = totals.merge(summed, on=["region", "scenario", "forecast_quarter"])
    assert len(merged) > 0
    assert (merged["forecast_handraisers"] == merged["summed"]).all()


def test_phi_outside_the_allowed_range_is_rejected():
    with pytest.raises(ValueError):
        damped_growth(anchor=0.0, g_shrunk=-0.1, phi=0.4, horizon=1)


def test_backtest_softens_a_one_quarter_shock():
    # The drop is already over by the next quarter. Copying it forward is the larger error.
    quarterly = _counted([100, 100, 100, 100, 40, 100, 100])
    summary = backtest(quarterly, CONFIG)
    plain, softened = _method_pair(summary)
    assert plain["n"] == 2
    assert softened["n"] == 2
    assert softened["mape"] < plain["mape"]


def test_published_history_leaves_fy27_q4_blank_and_lets_segments_sum():
    # Seven quarters cannot fill the quarter whose year-ago base has not closed.
    quarterly = pd.read_csv(Path(__file__).with_name("data") / "quarterly_handraisers.csv")
    forecast = prepare_forecast(quarterly, CONFIG)
    assert forecast.loc[forecast["forecast_quarter"] == "2027-Q4", "forecast_handraisers"].isna().all()
    segments = forecast[forecast["segment"] != "All segments"]
    totals = forecast[forecast["segment"] == "All segments"]
    summed = segments.groupby(["region", "scenario", "forecast_quarter"], as_index=False)["forecast_handraisers"].sum(
        min_count=1
    )
    merged = totals.merge(summed, on=["region", "scenario", "forecast_quarter"], suffixes=("_total", "_summed"))
    both_blank = merged["forecast_handraisers_total"].isna() & merged["forecast_handraisers_summed"].isna()
    matched = merged["forecast_handraisers_total"] == merged["forecast_handraisers_summed"]
    assert (both_blank | matched).all()


def test_backtest_reports_when_softening_is_worse():
    # The drop keeps going, so fading it toward zero misses the quarters that follow.
    quarterly = _counted([100, 100, 100, 100, 40, 30, 20])
    summary = backtest(quarterly, CONFIG)
    plain, softened = _method_pair(summary)
    assert softened["mape"] > plain["mape"]


def _method_pair(summary):
    segment = summary[summary["segment"] == "A"]
    plain = segment[segment["method"] == "plain_yoy"].iloc[0]
    softened = segment[segment["method"] == "softened"].iloc[0]
    return plain, softened


def _counted(counts):
    rows = []
    for index, leads in enumerate(counts):
        year, quarter = 2025 + (index // 4), (index % 4) + 1
        for segment in ("A", "All segments"):
            rows.append(
                {
                    "region": "US+LATAM+ANZ",
                    "segment": segment,
                    "fiscal_year": year,
                    "fiscal_quarter": quarter,
                    "handraisers": leads,
                }
            )
    return pd.DataFrame(rows)


def _panel(quarters, segment_leads):
    rows = []
    for index in range(quarters):
        year, quarter = 2024 + (index // 4), (index % 4) + 1
        for segment, leads in segment_leads.items():
            rows.append(
                {
                    "region": "US+LATAM+ANZ",
                    "segment": segment,
                    "fiscal_year": year,
                    "fiscal_quarter": quarter,
                    "handraisers": leads * (index + 1),
                }
            )
        rows.append(
            {
                "region": "US+LATAM+ANZ",
                "segment": "All segments",
                "fiscal_year": year,
                "fiscal_quarter": quarter,
                "handraisers": sum(segment_leads.values()) * (index + 1),
            }
        )
    return pd.DataFrame(rows)
