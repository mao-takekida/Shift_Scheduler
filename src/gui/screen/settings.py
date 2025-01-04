import logging
import sys
from pathlib import Path
from typing import Tuple

if str(Path(__file__).parents[2]) not in sys.path:
    print(sys.path)
    sys.path.append(str(Path(__file__).parents[2]))

import flet as ft

from gui.utils.file_picker import FilePicker
from gui.utils.text_fields_creator import TextFieldsCreator

logger = logging.getLogger("shift_scheduler")


class SettingsScreen:
    def __init__(self, page: ft.Page):
        self.page = page

    # 戻るボタン
    def _back_button(self) -> ft.ElevatedButton:
        # 循環参照を避けるため、ここでインポート
        from gui.screen.main_screen import MainScreen

        main_screen = MainScreen(self.page)
        back_button = ft.ElevatedButton(
            "戻る", on_click=lambda e: (self.page.clean(), main_screen.show_main())
        )
        return back_button

    # エクセルの設定
    def _excel_path(self) -> Tuple[ft.TextField, ft.ElevatedButton]:
        # テキストフィールドの初期値
        excel_path = TextFieldsCreator.create_text_field_read_only(
            label="Excelファイルのパス",
            value="",
        )

        def on_result(result: ft.FilePickerResultEvent):
            if result.files:
                excel_path.value = result.files[0].path
                self.page.update()

                logger.info(f"選択されたファイル: {excel_path.value}")
            else:
                logger.info("ファイルが選択されていません")

        # ファイル選択ボタン
        select_button = FilePicker.select_file_button(
            self.page, "ファイルを選択", on_result, allow_multiple=False
        )

        return excel_path, select_button

    def _on_change(self):
        self.page.update()

    def show_settings(self) -> None:
        """
        設定画面を表示し、さまざまな設定オプションを提供します。

        Args:
            page (ft.Page): 設定画面を表示する Flet ページオブジェクト。
        """
        self.page.clean()
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.vertical_alignment = ft.MainAxisAlignment.START

        # ボタン
        back_button = self._back_button()

        # エクセルの設定
        excel_path, select_button = self._excel_path()

        self.page.add(
            back_button,
            ft.Divider(),
            excel_path,
            select_button,
        )
