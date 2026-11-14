# APP: Table · Pipeline summary — native Hex table for the Overview section.
import pandas as pd

pipeline_summary = pd.DataFrame(
    {
        "metric": ["NB + Expansion total", "Open", "Won"],
        "amount_eur": [2461063, 2427423, 33640],
        "opps": [29, pd.NA, 3],
    }
)
pipeline_summary
