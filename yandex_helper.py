def get_headers(token: str, client_login: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Client-Login": f"{client_login}",
        "Accept-Language": "ru",
        "processingMode": "auto"

    }


def get_body(start_date, end_date) -> dict[str, dict[str, any]]:
    return {
        "params": {
            "SelectionCriteria": {
                "DateFrom": start_date,
                "DateTo": end_date,
            },
            "FieldNames": [
                "Date",
                "CampaignName",
                "Impressions",
                "Clicks",
                "Cost"
            ],
            "ReportName": f"CAMPAIGN_STATIC {start_date} - {end_date}",
            "ReportType": "CUSTOM_REPORT",
            "DateRangeType": "CUSTOM_DATE",
            "Format": "TSV",
            "IncludeVAT": "YES",  # включить НДС в стоимость
            "IncludeDiscount": "NO"
        }
    }
