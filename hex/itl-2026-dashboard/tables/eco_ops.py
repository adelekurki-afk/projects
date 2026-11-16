# APP: Table · Eco operations — native Hex table for the Feedback section.
import pandas as pd

eco_operations = pd.DataFrame(
    {
        "item": [
            "Registration and check-in",
            "Venue (Wilhelm Studios)",
            "Food and drinks",
            "Finding your way around",
            "Pre-event communication",
            "Audio/visual and room comfort",
        ],
        "mean_5": [4.53, 4.28, 4.35, 3.58, 3.95, 4.14],
        "n_rated": [43, 43, 43, 43, 42, 43],
        "top2_pct": [93.0, 79.1, 90.7, 53.5, 71.4, 76.7],
        "excellent": [30, 23, 22, 12, 15, 20],
        "very_good": [10, 11, 17, 11, 15, 13],
        "good": [1, 8, 2, 13, 8, 7],
        "fair": [0, 0, 1, 4, 3, 2],
        "poor": [2, 1, 1, 3, 1, 1],
    }
)
eco_operations
