import logging
from pathlib import Path
from typing import Dict, List, Tuple

import xlsxwriter

logger = logging.getLogger("shift_scheduler")


class ExcelWriter:
    def __init__(
        self, path: str, sheet_name: str, weights: Dict[str, float], fulltime: List[str]
    ):
        """
        ExcelWriterを初期化します。

        Args:
            path (str): 保存するExcelファイルのパス。
            sheet_name (str): シート名。
        """
        self.path = path
        self.sheet_name = sheet_name
        self.weights = weights
        self.fulltime = fulltime

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
            self._create_schedule_excel(schedule_list)
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

    def _get_formatted_worker_list(self, workers: List[str]) -> List[Tuple[str, dict]]:
        """
        従業員のリストをリッチテキスト形式で返します。

        Args:
            workers (List[str]): 従業員のリスト。

        Returns:
            List[Tuple[str, dict]]: 従業員の文字列とフォーマット情報のリスト。
        """
        # 重み順に並び替え
        workers = sorted(workers, key=lambda x: self.weights.get(x, 0), reverse=True)

        # リッチテキストの作成
        formatted_workers = []
        for worker in workers:
            if "不足" in worker or "未割当" in worker:
                # "不足"を含む場合は赤色のフォーマットを適用
                formatted_workers.append((worker, {"color": "red"}))
            # 社員がフルタイムの場合は青色のフォーマットを適用
            elif self.fulltime.get(worker, False):
                formatted_workers.append((worker, {"color": "green"}))
            else:
                # 通常のフォーマット
                formatted_workers.append((worker, {"color": "black"}))
            formatted_workers.append((", ", {}))  # カンマとスペースを追加

        if len(workers) >= 2:
            formatted_workers.pop()
        return formatted_workers

    def _create_schedule_excel(
        self, schedule_list: List[Tuple[str, Dict[str, List[str]]]]
    ):
        """
        指定されたスケジュールを使用してExcelファイルを作成し保存します。

        Args:
            schedule_list (List[Tuple[str, Dict[str, List[str]]]]): スケジュールのリスト。
        """
        # ワークブックとワークシートを作成
        workbook = xlsxwriter.Workbook(self.path)
        worksheet = workbook.add_worksheet(self.sheet_name)

        # ヘッダーを書き込む
        worksheet.write(0, 0, "Day")
        roles = list(schedule_list[0][1].keys())

        for col, role in enumerate(roles, start=1):
            worksheet.write(0, col, role)

        # スケジュールデータを書き込む
        for row_idx, (day_index, roles_dict) in enumerate(schedule_list, start=1):
            worksheet.write(row_idx, 0, day_index)  # 日付を記入

            for col_idx, role in enumerate(roles, start=1):
                workers = roles_dict.get(role, [])
                formatted_workers_parts = self._get_formatted_worker_list(workers)

                # リッチテキスト用のデータを構築
                cell_rich_text = []
                for part, fmt in formatted_workers_parts:
                    if "color" in fmt:
                        format_obj = workbook.add_format({"color": fmt["color"]})
                        cell_rich_text.append(format_obj)
                    cell_rich_text.append(part)

                if cell_rich_text:
                    worksheet.write_rich_string(row_idx, col_idx, *cell_rich_text)

        # ファイルを保存
        workbook.close()
