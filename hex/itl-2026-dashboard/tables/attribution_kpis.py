# APP: Table · Sourced vs influenced — native Hex table for the Funnel section.
import pandas as pd

attribution_kpis = pd.DataFrame(
    {
        "bucket": ["Sourced", "Influenced", "NB + Expansion pipeline"],
        "opps": [12, 18, 29],
        "amount_eur": [1011000, 1170491, 2461063],
        "won_opps": [1, 2, 3],
        "won_eur": [6400, 25640, 33640],
    }
)
attribution_kpis
