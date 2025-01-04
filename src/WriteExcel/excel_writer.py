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
        # if not self._confirm_overwrite():
        #     logger.info("スケジュールの書き込みを中止しました。")
        #     return

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

    def _write_workers_more_than_or_equal_to_two(
        self, workbook, worksheet, row_idx, col_idx, workers
    ):
        """
        2人以上の従業員が割り当てられている場合の処理を行います。

        Args:
            workbook (xlsxwriter.Workbook): ワークブック。
            worksheet (xlsxwriter.Worksheet): ワークシート。
            row_idx (int): 行インデックス。
            col_idx (int): 列インデックス。
            workers (List[str]): 従業員のリスト。
        """
        # セルのフォーマットを設定
        red_fmt = workbook.add_format({"color": "red"})
        green_fmt = workbook.add_format({"color": "green"})
        black_fmt = workbook.add_format({"color": "black"})

        # 重み順に並び替え
        workers = sorted(workers, key=lambda x: self.weights.get(x, 0), reverse=True)

        # セルに書き込むためのリストを作成
        rich_text = []
        for idx, worker in enumerate(workers):
            if "不足" in worker or "未割当" in worker:
                rich_text.append(red_fmt)
                rich_text.append(worker)
            elif self.fulltime.get(worker, False):
                rich_text.append(green_fmt)
                rich_text.append(worker)
            else:
                rich_text.append(black_fmt)
                rich_text.append(worker)
            # 最後の要素以外にはカンマとスペースを追加
            if idx < len(workers) - 1:
                rich_text.append(black_fmt)
                rich_text.append(", ")

        # セルにリッチテキストを書き込む
        worksheet.write_rich_string(row_idx, col_idx, *rich_text)

    def _write_workers_equal_to_one(
        self, workbook, worksheet, row_idx, col_idx, workers
    ):
        """
        1人の従業員が割り当てられている場合の処理を行います。
        write_rich_string が3つ以上のリストについてのみ可能なため

        Args:
            worksheet (xlsxwriter.Worksheet): ワークシート。
            row_idx (int): 行インデックス。
            col_idx (int): 列インデックス。
            workers (List[str]): 従業員のリスト。
        """
        worker = workers[0]

        cell_format = workbook.add_format()

        if "不足" in worker or "未割当" in worker:
            cell_format.set_font_color("red")
        elif self.fulltime.get(worker, False):
            cell_format.set_font_color("green")
        else:
            cell_format.set_font_color("black")

        worksheet.write(row_idx, col_idx, worker, cell_format)

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
                if len(workers) >= 2:
                    self._write_workers_more_than_or_equal_to_two(
                        workbook, worksheet, row_idx, col_idx, workers
                    )
                elif len(workers) == 1:
                    self._write_workers_equal_to_one(
                        workbook, worksheet, row_idx, col_idx, workers
                    )
                else:
                    pass

        # ファイルを保存
        workbook.close()
