#!/usr/bin/env python3
from pathlib import Path
from crash_proof import wrap_last_fig, wrap_display

ROOT = Path(__file__).resolve().parent
ORIG = ROOT / "original_app_cells"
OUT = ROOT / "wrapped_app_cells"
OUT.mkdir(exist_ok=True)

JOBS = [
    ("funnel.py", wrap_last_fig, ["lead_funnel"]),
    ("pipeline.py", wrap_last_fig, ["pipeline_arr"]),
    ("registrant_mix.py", wrap_last_fig, ["registrants"]),
    ("ga4_weekly.py", wrap_last_fig, ["ga4_signup_weekly"]),
    ("itl_pages.py", wrap_last_fig, ["ga4_itl_pages"]),
    ("group_kpi.py", wrap_last_fig, ["attendance_group_funnel"]),
    ("group_pipeline.py", wrap_last_fig, ["attendance_group_pipeline", "attendance_group_funnel"]),
    ("full_cab.py", wrap_display, ["lead_funnel", "pipeline_arr", "attendance_group_funnel", "attendance_group_pipeline"]),
    ("cab_roles.py", wrap_display, ["cab_overlay_kpis", "persona_by_role", "ga4_post_event_trend", "ga4_itl_weekly_pages"]),
]

for name, fn, frames in JOBS:
    src_path = ORIG / name
    if not src_path.exists():
        print("skip missing", name)
        continue
    wrapped = fn(src_path.read_text(), frames)
    (OUT / name).write_text(wrapped)
    compile(wrapped, str(OUT / name), "exec")
    print(f"wrapped {name}: {len(wrapped)} chars")
