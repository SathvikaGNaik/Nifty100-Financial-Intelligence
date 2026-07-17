VALIDATION_CONFIG = {
    "companies": {
        "required_columns": [
            "id",
            "company_name"
        ],
        "url_columns": [
            "website",
            "nse_profile",
            "bse_profile",
            "chart_link"
        ],
        "numeric_columns": [
            "face_value",
            "book_value",
            "roce_percentage",
            "roe_percentage"
        ]
    },

    "profitandloss": {
        "required_columns": ["id"],
        "numeric_columns": []
    },

    "balancesheet": {
        "required_columns": ["id"],
        "numeric_columns": []
    },

    "cashflow": {
        "required_columns": ["id"],
        "numeric_columns": []
    },

    "analysis": {
        "required_columns": ["id"]
    },

    "documents": {
        "required_columns": ["id"]
    }
}