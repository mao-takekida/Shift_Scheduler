import logging
from typing import Callable

import flet as ft

logger = logging.getLogger("shift_scheduler")


class FilePicker:
    @staticmethod
    def select_file_button(
        page: ft.Page,
        label: str,
        on_result: Callable[[ft.FilePickerResultEvent], None],
        allow_multiple: bool = True,
    ) -> ft.ElevatedButton:
        """
        ファイル選択ダイアログを開いてファイルを選択します。

        Args:
            page (ft.Page): ファイル選択ダイアログを表示する Flet ページオブジェクト。
            label (str): ボタンのラベル。
            on_result (Callable[[ft.FilePickerResultEvent], None]):
                ファイル選択時に呼び出されるコールバック関数。
            allow_multiple (bool, optional): 複数のファイルを選択できるかどうか。デフォルトは True。
        """

        def on_click(e):
            logger.debug("ファイル選択ダイアログを開きます。")
            picker = ft.FilePicker(on_result)
            if picker not in page.overlay:
                page.overlay.append(picker)
                page.update()
            # 一つだけ
            picker.pick_files(allow_multiple=allow_multiple)

        button = ft.ElevatedButton(label, on_click=on_click)
        return button
