# エクセルからデータを読みます。
import pandas as pd


class ExcelReader:
    def __init__(self, path):
        self.path = path

    # 一列目が名前、二列目以降が日付の希望シフト
    def read(self, sheet_name):
        df = pd.read_excel(self.path, sheet_name=sheet_name, index_col=0)
        return df

    def read_fulltime(self, sheet_name) -> dict:
        df = pd.read_excel(self.path, sheet_name=sheet_name, header=None)
        df.columns = ["name", "is_fulltime"]
        # ox -> True/False
        df["is_fulltime"] = df["is_fulltime"].apply(
            lambda x: True if x == "o" else False
        )
        fulltime_dict = {
            name: is_fulltime
            for name, is_fulltime in zip(df["name"], df["is_fulltime"])
        }
        return fulltime_dict
