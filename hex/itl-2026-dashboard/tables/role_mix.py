# APP: Table · Role mix — native Hex table for the Participation section.
import pandas as pd

role_mix = pd.DataFrame(
    {
        "cut": [
            "Segment · Unknown",
            "Segment · MM",
            "Segment · ENT",
            "Segment · SMB",
            "Seniority · Exec / founder",
            "Seniority · Manager / lead",
            "Seniority · IC / practitioner",
            "Seniority · Other",
            "Seniority · Director / head of",
            "Seniority · Partner / consultant",
            "Seniority · Unknown title",
            "Seniority · VP",
        ],
        "partner_day": [149, 138, 64, 52, 87, 83, 69, 61, 42, 28, 28, 4],
        "ecosystem_day": [343, 304, 158, 60, 130, 187, 206, 145, 90, 56, 45, 6],
    }
)
role_mix
