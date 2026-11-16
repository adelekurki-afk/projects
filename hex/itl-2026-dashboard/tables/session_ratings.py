# APP: Table · Session ratings — native Hex table for the Feedback section.
import pandas as pd

session_ratings = pd.DataFrame(
    {
        "session": [
            "Low-Pressure Networking for the n8n Community",
            "Building the Future of the Ambassador Program",
            "Building Autonomous Agents for Production",
            "Our Vision for What’s Next",
            "How to Host a Great n8n Event",
            "Inside n8n's Next Chapter",
            "Feature Kitchen: Agentic Context Layer",
            "Feature Kitchen: Credential Management",
            "We Didn’t Build an Agent Factory",
            "One Agent, Too Many Jobs: Rebuilding Nate",
            "Closing Words",
            "How We Got Here and Where We’re Going",
        ],
        "n": [6, 6, 5, 5, 4, 3, 3, 2, 2, 2, 2, 2],
        "session_mean": [5.00, 5.00, 5.00, 4.80, 5.00, 5.00, 4.67, 5.00, 5.00, 4.50, 5.00, 5.00],
        "speaker_mean": [5.83, 7.50, 6.40, 5.80, 5.00, 6.67, 6.33, 10.00, 9.00, 7.00, 5.00, 5.00],
    }
)
session_ratings
