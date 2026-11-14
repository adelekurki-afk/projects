# APP: Table · Speakers by day — native Hex table for the Participation section.
import pandas as pd

speakers_by_day = pd.DataFrame(
    {
        "day": ["Partner Day", "Ecosystem Day"],
        "speakers": [86, 79],
    }
)
speakers_by_day
