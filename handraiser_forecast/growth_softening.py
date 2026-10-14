"""Soften a steep year-over-year lead rate before it is used as a forecast.

Plain year-over-year copies last year's shock into next year. Shrinkage stops a
thin segment from outvoting the market, and damping lets that shock fade.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# One place to change the forecast. Scenarios override only phi and the anchor.
CONFIG = {
    "phi": 0.75,
    "phi_min": 0.5,
    "phi_max": 0.95,
    "anchor_mode": "median_8q",
    "anchor_min_quarters": 8,
    "fixed_anchor": 0.0,
    "floor": -0.20,
    "cap": 0.25,
    "horizons": 4,
    # None uses the median segment trailing-twelve-month volume.
    "k": None,
    "total_segment": "All segments",
    "scenarios": {
        "conservative": {"phi": 0.6, "anchor_cap_at_zero": True},
        "neutral": {},
        "optimistic": {"phi": 0.85},
    },
}


def shrinkage_weight(n: float, k: float) -> float:
    """A thin segment should borrow the market rate. k is the volume that counts as half trust."""
    if n + k <= 0:
        return 0.0
    return n / (n + k)


def shrunk_growth(segment_yoy: float, total_yoy: float, n: float, k: float) -> float:
    weight = shrinkage_weight(n, k)
    return weight * segment_yoy + (1.0 - weight) * total_yoy


def damped_growth(anchor: float, g_shrunk: float, phi: float, horizon: int) -> float:
    """A shock should matter less the further the quarter sits from today."""
    _require_phi(phi)
    if horizon < 1:
        raise ValueError("horizon starts at 1")
    return anchor + (g_shrunk - anchor) * (phi ** horizon)


def clamp_growth(growth: float, floor: float, cap: float) -> tuple[float, bool]:
    """Extreme rates are where a volatile quarter becomes an unusable forecast."""
    if growth > cap:
        return cap, True
    if growth < floor:
        return floor, True
    return growth, False


def prepare_forecast(quarterly: pd.DataFrame, config: dict | None = None) -> pd.DataFrame:
    """Build scenario rates from quarterly counts. The total row is the sum of segments."""
    cfg = CONFIG if config is None else config
    frame = quarterly.copy()
    frame["quarter_index"] = frame["fiscal_year"] * 4 + frame["fiscal_quarter"]
    rows = []
    for region, region_frame in frame.groupby("region", sort=False):
        rows.extend(_forecast_region(region, region_frame, cfg))
    columns = [
        "region",
        "segment",
        "scenario",
        "forecast_quarter",
        "ttm_yoy",
        "g_shrunk",
        "anchor",
        "phi",
        "g_final",
        "clamped_flag",
        "forecast_leads",
    ]
    return pd.DataFrame(rows, columns=columns)


def backtest(quarterly: pd.DataFrame, config: dict | None = None) -> pd.DataFrame:
    """Mean absolute percent error for plain year-over-year against the softened rate.

    A four-quarter holdout needs eight earlier quarters, which this history does
    not have. The score uses the first origin that already has a rate, then the
    later quarters that were actually observed. n is that count, not four.
    """
    detail = backtest_detail(quarterly, config)
    if detail.empty:
        return pd.DataFrame(columns=["region", "segment", "method", "n", "mape"])
    return (
        detail.groupby(["region", "segment", "method"], as_index=False)
        .agg(n=("abs_pct_error", "size"), mape=("abs_pct_error", "mean"))
    )


def backtest_detail(quarterly: pd.DataFrame, config: dict | None = None) -> pd.DataFrame:
    """One row per scored quarter, so a worse softened error can be seen rather than averaged away."""
    cfg = CONFIG if config is None else config
    frame = quarterly.copy()
    frame["quarter_index"] = frame["fiscal_year"] * 4 + frame["fiscal_quarter"]
    scored = []
    for region, region_frame in frame.groupby("region", sort=False):
        scored.extend(_backtest_region(region, region_frame, cfg))
    columns = [
        "region",
        "segment",
        "method",
        "origin_quarter",
        "quarter",
        "actual",
        "prediction",
        "abs_pct_error",
    ]
    return pd.DataFrame(scored, columns=columns)


def shrinkage_k(volumes: pd.Series, config: dict) -> float:
    """k is a volume, not a weight. The median keeps a thin segment from being fully trusted."""
    if config["k"] is not None:
        return float(config["k"])
    return float(np.median(volumes.to_numpy()))


def _forecast_region(region: str, region_frame: pd.DataFrame, config: dict) -> list[dict]:
    total_name = config["total_segment"]
    series = {
        segment: group.set_index("quarter_index")["leads"].sort_index()
        for segment, group in region_frame.groupby("segment", sort=False)
    }
    if total_name not in series:
        # The market rate has to exist even if the extract forgot the total row.
        segment_names = [name for name in series if name != total_name]
        stacked = pd.concat([series[name] for name in segment_names], axis=1).fillna(0)
        series[total_name] = stacked.sum(axis=1)

    latest_index = max(values.index.max() for values in series.values())
    segment_names = [name for name in series if name != total_name]
    volumes = {name: _trailing_volume(series[name], latest_index) for name in segment_names}
    k = shrinkage_k(pd.Series(volumes), config)
    rates = {name: _base_rate(series[name], latest_index) for name in list(series)}
    total_rate = rates[total_name]
    shrunk = {
        name: shrunk_growth(rates[name], total_rate, volumes[name], k)
        for name in segment_names
        if rates[name] is not None and total_rate is not None
    }
    forecast_quarters = _next_fiscal_year(latest_index)
    segment_rows = []
    for scenario, overrides in config["scenarios"].items():
        phi = overrides.get("phi", config["phi"])
        for segment in segment_names:
            if segment not in shrunk:
                continue
            anchor = _anchor(series[segment], latest_index, config, overrides)
            for horizon, (year, quarter) in enumerate(forecast_quarters, start=1):
                raw = damped_growth(anchor, shrunk[segment], phi, horizon)
                final, flagged = clamp_growth(raw, config["floor"], config["cap"])
                base = _leads_at(series[segment], year - 1, quarter)
                leads = None if base is None else _round_half_up(base * (1.0 + final))
                segment_rows.append(
                    {
                        "region": region,
                        "segment": segment,
                        "scenario": scenario,
                        "forecast_quarter": f"{year}-Q{quarter}",
                        "ttm_yoy": rates[segment],
                        "g_shrunk": shrunk[segment],
                        "anchor": anchor,
                        "phi": phi,
                        "g_final": final,
                        "clamped_flag": flagged,
                        "forecast_leads": leads,
                        "base_leads": base,
                        "horizon": horizon,
                    }
                )
    # The published total has to be the segments, or a shrunk total would not match them.
    totals = []
    keyed = pd.DataFrame(segment_rows)
    if keyed.empty:
        return []
    for (scenario, forecast_quarter), group in keyed.groupby(["scenario", "forecast_quarter"], sort=False):
        sample = group.iloc[0]
        overrides = config["scenarios"][scenario]
        complete = group["forecast_leads"].notna().all() and group["base_leads"].notna().all()
        base_sum = group["base_leads"].sum() if complete else None
        if complete and base_sum:
            leads = int(group["forecast_leads"].sum())
            # The total's rate is the volume result, because each segment was clamped on its own.
            implied = leads / float(base_sum) - 1.0
        else:
            leads = None
            implied = None
        totals.append(
            {
                "region": region,
                "segment": total_name,
                "scenario": scenario,
                "forecast_quarter": forecast_quarter,
                "ttm_yoy": total_rate,
                "g_shrunk": total_rate,
                "anchor": _anchor(series[total_name], latest_index, config, overrides),
                "phi": sample["phi"],
                "g_final": implied,
                "clamped_flag": bool(group["clamped_flag"].any()),
                "forecast_leads": leads,
                "base_leads": None if base_sum is None else base_sum,
                "horizon": int(sample["horizon"]),
            }
        )
    combined = segment_rows + totals
    for row in combined:
        row.pop("horizon", None)
        row.pop("base_leads", None)
    return combined


def _backtest_region(region: str, region_frame: pd.DataFrame, config: dict) -> list[dict]:
    """Score from one origin so the same actual is not counted once per earlier quarter."""
    total_name = config["total_segment"]
    indexes = sorted(int(index) for index in region_frame["quarter_index"].unique())
    series = {
        segment: group.set_index("quarter_index")["leads"].sort_index()
        for segment, group in region_frame.groupby("segment", sort=False)
    }
    if total_name not in series:
        return []
    origin = next(
        (index for index in indexes if _base_rate(series[total_name], index) is not None),
        None,
    )
    if origin is None:
        return []
    rates = {name: _base_rate(values, origin) for name, values in series.items()}
    if rates.get(total_name) is None:
        return []
    volumes = {
        name: _trailing_volume(values, origin)
        for name, values in series.items()
        if name != total_name
    }
    k = shrinkage_k(pd.Series(volumes), config)
    origin_year, origin_quarter = _split_index(origin)
    scored = []
    for target in indexes:
        step = target - origin
        if step < 1 or step > config["horizons"]:
            continue
        target_year, target_quarter = _split_index(target)
        quarter_label = f"{target_year}-Q{target_quarter}"
        for segment, values in series.items():
            if segment == total_name or rates.get(segment) is None:
                continue
            actual = _value(values, target)
            base = _value(values, target - 4)
            if actual is None or actual == 0 or base is None:
                continue
            plain = base * (1.0 + rates[segment])
            g_shrunk = shrunk_growth(rates[segment], rates[total_name], volumes[segment], k)
            anchor = _anchor(values, origin, config, {})
            final, _flagged = clamp_growth(
                damped_growth(anchor, g_shrunk, config["phi"], step),
                config["floor"],
                config["cap"],
            )
            softened = base * (1.0 + final)
            for method, prediction in (("plain_yoy", plain), ("softened", softened)):
                scored.append(
                    {
                        "region": region,
                        "segment": segment,
                        "method": method,
                        "origin_quarter": f"{origin_year}-Q{origin_quarter}",
                        "quarter": quarter_label,
                        "actual": actual,
                        "prediction": prediction,
                        "abs_pct_error": abs(prediction - actual) / actual,
                    }
                )
    return scored


def _base_rate(leads: pd.Series, latest_index: int) -> float | None:
    """Prefer a trailing-twelve-month rate. A single quarter is the rate we have until then."""
    ttm_yoy = _ttm_yoy(leads, latest_index)
    if ttm_yoy is not None:
        return ttm_yoy
    return _same_quarter_yoy(leads, latest_index)


def _ttm_yoy(leads: pd.Series, latest_index: int) -> float | None:
    current = _sum_window(leads, latest_index, 4)
    prior = _sum_window(leads, latest_index - 4, 4)
    if current is None or prior is None or prior == 0:
        return None
    return current / prior - 1.0


def _same_quarter_yoy(leads: pd.Series, latest_index: int) -> float | None:
    current = _value(leads, latest_index)
    prior = _value(leads, latest_index - 4)
    if current is None or prior is None or prior == 0:
        return None
    return current / prior - 1.0


def _trailing_volume(leads: pd.Series, latest_index: int) -> float:
    """Shrinkage should use a year of volume. The latest quarter stands in until four exist."""
    window = _sum_window(leads, latest_index, 4)
    if window is not None:
        return window
    latest = _value(leads, latest_index)
    return 0.0 if latest is None else latest


def _sum_window(leads: pd.Series, end_index: int, length: int) -> float | None:
    indexes = [end_index - offset for offset in range(length)]
    if any(index not in leads.index for index in indexes):
        return None
    return float(sum(leads.loc[index] for index in indexes))


def _anchor(leads: pd.Series, latest_index: int, config: dict, overrides: dict) -> float:
    """The long-run rate should not be one noisy year. Eight trailing rates are the minimum."""
    mode = overrides.get("anchor_mode", config["anchor_mode"])
    if isinstance(mode, (int, float)) and not isinstance(mode, bool):
        anchor = float(mode)
    elif mode == "zero":
        anchor = 0.0
    elif mode == "median_8q":
        history = []
        for index in range(latest_index, latest_index - 12, -1):
            rate = _ttm_yoy(leads, index)
            if rate is not None:
                history.append(rate)
            if len(history) == config["anchor_min_quarters"]:
                break
        anchor = float(np.median(history)) if len(history) >= config["anchor_min_quarters"] else 0.0
    else:
        anchor = float(config["fixed_anchor"])
    if overrides.get("anchor_cap_at_zero"):
        anchor = min(anchor, 0.0)
    return anchor


def _next_fiscal_year(latest_index: int) -> list[tuple[int, int]]:
    year, _quarter = _split_index(latest_index)
    return [(year + 1, quarter) for quarter in range(1, 5)]


def _split_index(index: int) -> tuple[int, int]:
    return (index - 1) // 4, (index - 1) % 4 + 1


def _leads_at(leads: pd.Series, year: int, quarter: int) -> float | None:
    return _value(leads, year * 4 + quarter)


def _value(leads: pd.Series, index: int) -> float | None:
    if index not in leads.index:
        return None
    return float(leads.loc[index])


def _require_phi(phi: float) -> None:
    if not CONFIG["phi_min"] <= phi <= CONFIG["phi_max"]:
        raise ValueError(f"phi must be between {CONFIG['phi_min']} and {CONFIG['phi_max']}")


def _round_half_up(value: float) -> int:
    return int(np.floor(value + 0.5))


def main() -> None:
    from pathlib import Path

    root = Path(__file__).resolve().parent
    quarterly = pd.read_csv(root / "data" / "quarterly_handraisers.csv")
    forecast = prepare_forecast(quarterly)
    detail = backtest_detail(quarterly)
    summary = backtest(quarterly)
    output = root / "output"
    output.mkdir(exist_ok=True)
    # Nullable integers keep a missing quarter blank instead of turning it into zero.
    forecast["forecast_leads"] = forecast["forecast_leads"].astype("Int64")
    forecast.to_csv(output / "forecast_growth.csv", index=False, na_rep="")
    summary.to_csv(output / "backtest_mape.csv", index=False)
    detail.to_csv(output / "backtest_detail.csv", index=False)
    _print_backtest(summary)


def _print_backtest(summary: pd.DataFrame) -> None:
    if summary.empty:
        print("No quarters could be scored.")
        return
    wide = summary.pivot(index=["region", "segment"], columns="method", values="mape")
    wide["n"] = summary.groupby(["region", "segment"])["n"].first()
    wide["softened_worse"] = wide["softened"] > wide["plain_yoy"]
    print(wide.to_string())
    print(f"segments where softened MAPE is worse: {int(wide['softened_worse'].sum())} of {len(wide)}")


if __name__ == "__main__":
    main()
