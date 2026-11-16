# APP: Table · Also on site — native Hex table for the Participation section.
import pandas as pd

also_on_site = pd.DataFrame(
    {
        "item": [
            "Staff tickets",
            "Programme speakers",
            "CAB",
            "Fliplet booked meetings",
            "Meeting arrivals",
            "Sales meetings sheet",
            "Salesforce meeting booked",
            "Ecosystem recommend (n=43, NPS 72)",
            "Partner Day overall (n=23)",
            "Session rating (n=66)",
        ],
        "value": [113, 116, 39, 1076, 425, 23, 20, 9.1, 8.8, 4.8],
        "unit": [
            "tickets",
            "speakers",
            "people",
            "bookings",
            "arrivals",
            "people",
            "campaign members",
            "score /10",
            "score /10",
            "score /5",
        ],
        "note": [
            "Overlay inside 426 / 916, not extra headcount",
            "Overlay inside 426 / 916, not extra headcount",
            "11 members · 28 guests",
            "Fliplet bookings clock",
            "Arrivals clock",
            "n8n sales sheet",
            "Salesforce CampaignMember",
            "Shared Fliplet workbook",
            "Shared Fliplet workbook",
            "Session ratings 4.8/5",
        ],
    }
)
also_on_site
