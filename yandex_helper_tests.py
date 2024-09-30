import unittest

from const import TOKEN, CLIENT_LOGIN
from yandex_helper import get_headers, get_body


class ReportTest(unittest.TestCase):
    def test_get_headers(self):
        self.assertEqual(
            get_headers(TOKEN, CLIENT_LOGIN),
            {
                "Authorization": "Bearer y0_AgAAAABRzx-eAAx-iAAAAAESFadrAACvJsMMAxFKG7ktyCnZ4FkX9gWbnQ",
                "Client-Login": "Sima-land-promo-person",
                "Accept-Language": "ru",
                "processingMode": "auto"
            }
        )

    def test_get_body(self):
        self.assertEqual(
            get_body("2024-01-01", "2024-01-31"),
            {
                "params": {
                    "SelectionCriteria": {
                        "DateFrom": "2024-01-01",
                        "DateTo": "2024-01-31"
                    },
                    "FieldNames": [
                        "Date",
                        "CampaignName",
                        "Impressions",
                        "Clicks",
                        "Cost"
                    ],
                    "ReportName": "CAMPAIGN_STATIC 2024-01-01 - 2024-01-31",
                    "ReportType": "CUSTOM_REPORT",
                    "DateRangeType": "CUSTOM_DATE",
                    "Format": "TSV",
                    'IncludeDiscount': 'NO',
                    'IncludeVAT': 'YES',
                }})
