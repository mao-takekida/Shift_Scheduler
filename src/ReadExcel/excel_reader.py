# エクセルからデータを読みます。
from typing import Dict

import pandas as pd


class ExcelReader:
    def __init__(self, path):
        self.path = path

    # 一列目が名前、二列目以降が日付の希望シフト
    def read(self, sheet_name: str) -> pd.DataFrame:
        df = pd.read_excel(self.path, sheet_name=sheet_name, index_col=0)
        return df

    def read_availabilities(self, sheet_name: str) -> Dict[str, Dict[str, bool]]:
        df = self.read(sheet_name)
        availability = dict(df.apply(lambda x: x.dropna().to_dict(), axis=1))
        # ox を True/False に変換
        availability = {
            name: {
                # 大文字小文字を区別しない
                # 空白を削除
                day: True if ox.strip().lower() == "o" else False
                for day, ox in availability[name].items()
            }
            for name in availability
        }
        return availability

    def read_capabilities(self, sheet_name: str) -> Dict[str, Dict[str, bool]]:
        df = self.read(sheet_name)
        capabilities = dict(df.apply(lambda x: x.dropna().to_dict(), axis=1))
        # ox を True/False に変換
        capabilities = {
            name: {
                # 大文字小文字を区別しない
                # 空白を削除
                role: True if ox.strip().lower() == "o" else False
                for role, ox in capabilities[name].items()
            }
            for name in capabilities
        }
        return capabilities

    def read_fulltime(self, sheet_name) -> dict:
        df = pd.read_excel(self.path, sheet_name=sheet_name, header=None)
        df.columns = ["name", "is_fulltime"]
        # ox -> True/False
        df["is_fulltime"] = df["is_fulltime"].apply(
            # 大文字小文字を区別しない
            # 空白を削除
            lambda x: True if x.strip().lower() == "o" else False
        )
        fulltime_dict = {
            name: is_fulltime
            for name, is_fulltime in zip(df["name"], df["is_fulltime"])
        }
        return fulltime_dict
