import logging
from pathlib import Path
from typing import Dict, List, Tuple

import xlsxwriter

logger = logging.getLogger("shift_scheduler")


class ExcelWriter:
    def __init__(self, path: str, sheet_name: str):
        """
        ExcelWriterを初期化します。

        Args:
            path (str): 保存するExcelファイルのパス。
            sheet_name (str): シート名。
        """
        self.path = path
        self.sheet_name = sheet_name

    def write_schedule(self, schedule_list: List[Tuple[str, Dict[str, List[str]]]]):
        """
        スケジュールをExcelファイルに書き込みます。

        Args:
            schedule_list (List[Tuple[str, Dict[str, List[str]]]]): スケジュールのリスト。
                フォーマット: [(day_index, {role: [worker1, worker2, ...]})]
        """
        if not self._confirm_overwrite():
            logger.info("スケジュールの書き込みを中止しました。")
            return

        try:
            self._create_excel(schedule_list)
            logger.info("スケジュールが正常に書き込まれました。")
        except Exception as e:
            logger.error(f"スケジュールの書き込み中にエラーが発生しました: {e}")
            raise

    def _confirm_overwrite(self) -> bool:
        """
        既存のファイルを上書きするかどうかを確認します。

        Returns:
            bool: 上書きを確認した場合はTrue、それ以外はFalse。
        """
        if Path(self.path).exists():
            while True:
                answer = (
                    input(f"{self.path} は既に存在します。上書きしますか？ [y/n]: ")
                    .strip()
                    .lower()
                )
                if answer in {"yes", "y"}:
                    return True
                elif answer in {"no", "n"}:
                    return False
                else:
                    logger.warning("'yes' または 'no' を入力してください。")
        return True

    def _create_excel(self, schedule_list: List[Tuple[str, Dict[str, List[str]]]]):
        """
        指定されたスケジュールを使用してExcelファイルを作成し保存します。

        Args:
            schedule_list (List[Tuple[str, Dict[str, List[str]]]]): スケジュールのリスト。
        """
        workbook = xlsxwriter.Workbook(self.path)
        worksheet = workbook.add_worksheet(self.sheet_name)

        # ヘッダーを書き込む
        worksheet.write(0, 0, "Day")
        roles = list(schedule_list[0][1].keys())

        for col, role in enumerate(roles, start=1):
            worksheet.write(0, col, role)

        # スケジュールデータを書き込む
        for row_idx, (day_index, roles_dict) in enumerate(schedule_list, start=1):
            worksheet.write(row_idx, 0, day_index)
            for col_idx, role in enumerate(roles, start=1):
                workers = ", ".join(roles_dict.get(role, []))
                worksheet.write(row_idx, col_idx, workers)

        workbook.close()
