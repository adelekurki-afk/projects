# APP: Table · Opportunities by type and segment — native Hex table.
import pandas as pd

opportunities_by_segment = pd.DataFrame(
    {
        "opp_type": ["New Business", "New Business", "Expansion", "Expansion"],
        "segment": ["ENT", "MM", "ENT", "MM"],
        "opps": [5, 12, 4, 8],
        "total_eur": [834000, 619200, 516150, 491713],
        "open_eur": [826000, 597200, 516150, 488073],
        "won_eur": [8000, 22000, 0, 3640],
    }
)
opportunities_by_segment
