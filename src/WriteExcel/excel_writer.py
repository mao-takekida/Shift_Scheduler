import logging
from typing import Dict, List

import xlsxwriter

logger = logging.getLogger("shift_scheduler")


class ExcelWriter:
    def __init__(self, path: str, sheet_name: str):
        """
        ExcelWriterを初期化します。

        Args:
            path (str): Excelファイルの保存先パス。
            sheet_name (str): シート名。
        """
        self.path = path
        self.sheet_name = sheet_name

    def write_schedule(self, days: List[int], schedule: List[Dict[str, str]]):
        """
        スケジュールをExcelに書き込みます。

        Args:
            days (List[int]): 日付リスト。
            schedule (List[Dict[str, str]]): 各日の役割と担当者のリスト。
        """
        try:
            workbook = xlsxwriter.Workbook(self.path)
            worksheet = workbook.add_worksheet(self.sheet_name)

            # ヘッダー行に見出しを記載
            worksheet.write(0, 0, "Day")
            roles = list(schedule[0].keys())

            for col, role in enumerate(roles, start=1):
                worksheet.write(0, col, role)

            # データ行にスケジュールを記載
            for i, day in enumerate(days, start=1):  # 行は 1 からスタート
                # 数値として
                worksheet.write(i, 0, day)
                for j, role in enumerate(roles, start=1):  # 列は 1 からスタート
                    worksheet.write(i, j, schedule[i - 1].get(role, ""))

            workbook.close()
            logger.info("スケジュールが正常に書き込まれました。")

        except Exception as e:
            logger.error(f"スケジュールの書き込み中にエラーが発生しました: {e}")
            raise
