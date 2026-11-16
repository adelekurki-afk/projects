# APP: Table · Staff by crew — native Hex table for the Participation section.
import pandas as pd

staff_by_crew = pd.DataFrame(
    {
        "crew": [
            "C2",
            "Hospitality / QT Events",
            "Content / merch / film",
            "n8n (staff ticket)",
            "Other crew",
        ],
        "registered": [40, 36, 19, 13, 5],
        "partner_day": [0, 8, 1, 6, 3],
        "eco_day": [2, 6, 2, 8, 1],
    }
)
staff_by_crew
