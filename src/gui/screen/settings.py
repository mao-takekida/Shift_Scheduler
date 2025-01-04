import logging
from typing import Any, Callable, Tuple

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


class TextFieldsCreator:

    @staticmethod
    def create_text_field_editable(
        label: str,
        value: str,
        on_change: Callable[[Any], None] = None,
        visible: bool = True,
    ) -> ft.TextField:
        """
        編集可能なテキストフィールドを生成します。

        Args:
            label (str): テキストフィールドのラベル。
            value (str): テキストフィールドの初期値。
            on_change (Callable[[Any], None], optional):
                値の変更時にトリガーされるコールバック関数。デフォルトは None。
            visible (bool, optional): テキストフィールドの表示状態。デフォルトは True。

        Returns:
            ft.TextField: 編集可能なテキストフィールドインスタンス。
        """
        return ft.TextField(
            label=label,
            value=value,
            on_change=on_change,
            visible=visible,
        )

    @staticmethod
    def create_text_field_read_only(
        label: str,
        value: str,
        on_change: Callable[[Any], None] = None,
        visible: bool = True,
    ) -> ft.TextField:
        """
        読み取り専用のテキストフィールドを生成します。

        Args:
            label (str): テキストフィールドのラベル。
            value (str): テキストフィールドの初期値。
            on_change (Callable[[Any], None], optional):
                値の変更時にトリガーされるコールバック関数。デフォルトは None。
            visible (bool, optional): テキストフィールドの表示状態。デフォルトは True。

        Returns:
            ft.TextField: 読み取り専用のテキストフィールドインスタンス。
        """
        return ft.TextField(
            label=label,
            value=value,
            on_change=on_change,
            visible=visible,
            read_only=True,
            text_style=ft.TextStyle(color=ft.colors.GREY_700),
            bgcolor=ft.colors.GREY_200,
            border=ft.InputBorder.NONE,
            hint_text="選択されていません",
            max_length=100,
            keyboard_type=ft.KeyboardType.TEXT,
        )


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
