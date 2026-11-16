# APP: Table · Attendance by region — native Hex table. Restyle in the App with the chart icon.
import pandas as pd

attendance_region = pd.DataFrame(
    {
        "region": ["DACH", "North EMEA", "South EMEA", "US", "Other"],
        "partner_day": [121, 29, 35, 22, 196],
        "ecosystem_day": [448, 63, 53, 42, 261],
    }
)
attendance_region
