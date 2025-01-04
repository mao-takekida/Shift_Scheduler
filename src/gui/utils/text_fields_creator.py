from typing import Any, Callable

import flet as ft


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
