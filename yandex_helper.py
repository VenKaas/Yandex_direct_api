from const import TOKEN, CLIENT_LOGIN


def get_headers(TOKEN, CLIENT_LOGIN) -> dict[str, str]:
    return {
        # OAuth-токен. Использование слова Bearer обязательно
        "Authorization": f"Bearer {TOKEN}",
        # Логин клиента рекламного агентства
        "Client-Login": CLIENT_LOGIN,
        # Язык ответных сообщений
        "Accept-Language": "ru",
        # Режим формирования отчета
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
