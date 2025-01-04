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
from utils.config import load_config, save_config

logger = logging.getLogger("shift_scheduler")


class SettingsScreen:
    def __init__(self, page: ft.Page):
        self.page = page
        self.config = load_config()

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
        excel_path_field = TextFieldsCreator.create_text_field_read_only(
            label="Excelファイルのパス",
            value=self.config.get("excel_path", ""),
        )

        def on_result(result: ft.FilePickerResultEvent):
            if result.files:
                logger.info(f"選択されたファイル: {result.files[0].path}")
                self.config["excel_path"] = result.files[0].path
                excel_path_field.value = result.files[0].path
                self._change_settings()
            else:
                logger.info("ファイルが選択されていません")

        # ファイル選択ボタン
        select_button = FilePicker.select_file_button(
            self.page, "ファイルを選択", on_result, allow_multiple=False
        )

        return excel_path_field, select_button

    def _output_dir(self) -> Tuple[ft.TextField, ft.ElevatedButton]:
        # テキストフィールドの初期値
        output_dir_field = TextFieldsCreator.create_text_field_read_only(
            label="出力フォルダ",
            value=self.config.get("output_dir", ""),
        )

        def on_result(result: ft.FilePickerResultEvent):
            if result.path:
                logger.info(f"選択されたディレクトリ: {result.path}")
                self.config["output_dir"] = result.path
                output_dir_field.value = result.path
                self._change_settings()
            else:
                logger.info("ディレクトリが選択されていません")

        # フォルダ選択ボタン
        select_button = FilePicker.select_file_button(
            self.page, "フォルダを選択", on_result, allow_multiple=False, is_dir=True
        )

        return output_dir_field, select_button

    # 試行回数の設定
    def _num_of_trials(self) -> Tuple[ft.TextField, ft.ElevatedButton]:
        # テキストフィールドの初期値
        num_of_trials_field = TextFieldsCreator.create_text_field_editable(
            label="試行回数",
            value=self.config.get("num_trials", "1"),
        )

        def on_change(e):
            if e.control.value.isdigit():
                logger.info(f"試行回数を設定します: {e.control.value}")
                self.config["num_trials"] = int(e.control.value)
                self._change_settings()
            else:
                logger.info("試行回数は整数でなければなりません")

        num_of_trials_field.on_change = on_change
        return num_of_trials_field

    def _change_settings(self):
        logger.debug(f"設定を保存します: {self.config}")
        save_config(self.config)
        self.page.update()

    def _setup_page(self):
        self.page.clean()
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.vertical_alignment = ft.MainAxisAlignment.START

    def show_settings(self) -> None:
        """
        設定画面を表示し、さまざまな設定オプションを提供します。

        Args:
            page (ft.Page): 設定画面を表示する Flet ページオブジェクト。
        """
        self._setup_page()

        # 戻るボタン
        back_button = self._back_button()
        excel_path_field, excel_select_button = self._excel_path()
        output_dir_field, outputdir_select_button = self._output_dir()
        num_of_trials_field = self._num_of_trials()

        self.page.add(
            back_button,
            ft.Divider(),
            excel_path_field,
            excel_select_button,
            ft.Divider(),
            output_dir_field,
            outputdir_select_button,
            ft.Divider(),
            num_of_trials_field,
        )
