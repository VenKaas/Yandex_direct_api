from abc import ABC, abstractmethod
from io import StringIO

import pandas as pd


class Storage(ABC):
    @abstractmethod
    def save_report(self, report: str, start_date: str, end_date: str):
        pass


class FileStorage(Storage):
    def save_report(self, report: str, start_date: str, end_date: str):
        with open(f'report-{start_date}-{end_date}.csv', 'w') as f:
            f.write(report)


class PandasStorage(Storage):
    def save_report(self, report: str, start_date: str, end_date: str):
        report_table = pd.read_csv(StringIO(report), delimiter='\t', skiprows=1)
        report_table['CTR'] = report_table.apply(lambda row: row['Impressions'] / row['Clicks'] if row['Clicks'] != 0 else 0, axis=1)
        report_table.to_csv(f'report-{start_date}-{end_date}.csv', index=False)


class MemoryStorage(Storage):

    def save_report(self, report: str, start_date: str, end_date: str):
        pass
