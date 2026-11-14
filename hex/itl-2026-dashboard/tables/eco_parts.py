# APP: Table · Eco programme parts — native Hex table for the Feedback section.
import pandas as pd

eco_programme_parts = pd.DataFrame(
    {
        "part": [
            "Opening keynote",
            "Talks and panels",
            "Lightning talks",
            "Feature Kitchens",
            "Community Lounge",
            "Market floor",
            "Networking time",
            "After-party",
        ],
        "mean_5": [3.97, 3.98, 3.59, 4.12, 3.92, 3.84, 4.00, 4.10],
        "n_rated": [38, 41, 27, 25, 26, 38, 39, 30],
        "top2_pct": [76.3, 78.0, 55.6, 76.0, 69.2, 63.2, 66.7, 73.3],
        "excellent": [9, 10, 3, 10, 9, 12, 14, 13],
        "very_good": [20, 22, 12, 9, 9, 12, 12, 9],
        "good": [8, 7, 10, 5, 6, 11, 12, 6],
        "fair": [1, 2, 2, 1, 1, 2, 1, 2],
        "poor": [0, 0, 0, 0, 1, 1, 0, 0],
        "did_not_attend": [5, 2, 16, 18, 17, 5, 4, 13],
    }
)
eco_programme_parts
