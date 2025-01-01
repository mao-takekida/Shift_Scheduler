# エクセルからデータを読みます。
import pandas as pd

class ExcelReader:
    def __init__(self, path):
        self.path = path

    # 一行目をヘッダーとして読み込む
    def read(self, sheet_name: str) -> pd.DataFrame:
        return pd.read_excel(self.path, sheet_name=sheet_name, header=0)