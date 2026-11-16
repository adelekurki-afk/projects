# APP: Table · Partner tracks — native Hex table for the Feedback section.
import pandas as pd

partner_tracks = pd.DataFrame(
    {
        "track": ["Solution Partners", "Ambassadors", "Node Partners"],
        "attended": [13, 8, 4],
        "content_mean": [8.46, 8.33, 7.50],
        "content_n": [13, 9, 4],
        "helps_work_closer": [8.69, 8.44, 7.25],
    }
)
partner_tracks
