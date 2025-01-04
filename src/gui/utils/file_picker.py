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
        is_dir: bool = False,
    ) -> ft.ElevatedButton:
        """
        ファイル選択ダイアログを開いてファイルを選択します。

        Args:
            page (ft.Page): ファイル選択ダイアログを表示する Flet ページオブジェクト。
            label (str): ボタンのラベル。
            on_result (Callable[[ft.FilePickerResultEvent], None]):
                ファイル選択時に呼び出されるコールバック関数。
            allow_multiple (bool, optional): 複数のファイルを選択できるかどうか。デフォルトは True。
            is_dir (bool, optional): ディレクトリを選択するかどうか。デフォルトは False。
        """

        def on_click(e):
            logger.debug("ファイル選択ダイアログを開きます。")
            picker = ft.FilePicker(on_result)
            if picker not in page.overlay:
                page.overlay.append(picker)
                page.update()

            # 選択する
            if is_dir:
                # ディレクトリ選択 (一つのみ)
                picker.get_directory_path()
            else:
                # ファイル選択
                picker.pick_files(allow_multiple=allow_multiple)

        button = ft.ElevatedButton(label, on_click=on_click)
        return button
