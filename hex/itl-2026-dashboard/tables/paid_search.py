# APP: Table · Paid search terms — native Hex table for the Intent section.
import pandas as pd

paid_search_terms = pd.DataFrame(
    {
        "term": [
            "n8n",
            "ai",
            "claude ai",
            "best business ai",
            "best ai for business",
            "n8n ai",
            "n8n login",
            "n8n workflows",
            "ai platforms",
            "ai for work",
            "n8n pricing",
            "ai for businesses",
            "what is n8n",
            "n8n cloud",
            "n8n automation",
        ],
        "impressions": [56162, 9751, 2753, 2336, 1381, 1369, 1247, 1109, 980, 969, 855, 805, 757, 556, 395],
        "clicks": [24376, 434, 186, 1283, 735, 650, 627, 468, 526, 496, 538, 423, 52, 265, 118],
        "cost": [
            16650.13, 1161.03, 920.24, 1485.32, 647.39, 608.77, 295.09, 621.32,
            475.23, 376.33, 648.79, 375.67, 58.45, 359.89, 93.84,
        ],
    }
)
paid_search_terms
