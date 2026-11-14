# APP: Table · Eco who answered — native Hex table for the Feedback section.
import pandas as pd

eco_who_answered = pd.DataFrame(
    {
        "role": [
            "Developer or engineer",
            "Founder, freelancer or agency",
            "IT, platform or security",
            "Business leader or decision-maker",
            "Automation or ops lead",
            "Consultant or implementation partner",
            "Community contributor or ambassador",
            "Other",
        ],
        "n": [10, 7, 6, 6, 5, 4, 2, 2],
    }
)
eco_who_answered
