# APP: Table · Visits — native Hex table for the Overview section.
import pandas as pd

visits = pd.DataFrame(
    {
        "metric": [
            "Registered",
            "Came · Partner Day",
            "Came · Ecosystem Day",
            "Unique people",
            "Both days",
            "Staff tickets",
            "Programme speakers",
            "CAB overlay",
        ],
        "people": [1269, 426, 916, 1018, 324, 113, 116, 39],
        "how_built": [
            "Paid + Free unique email",
            "13 Oct · 391 door + 35 badge",
            "14 Oct · 878 door + 38 green YES",
            "426 + 916 − 324 both days",
            "Inside both 426 and 916",
            "Overlay, not extra headcount",
            "Overlay, not extra headcount",
            "11 members · 28 guests",
        ],
    }
)
visits
