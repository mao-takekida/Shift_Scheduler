import logging

import flet as ft

logger = logging.getLogger("shift_scheduler")


# -------------------------------
# 設定画面の表示
# -------------------------------
def show_settings(page: ft.Page) -> None:
    """
    設定画面を表示し、さまざまな設定オプションを提供します。

    Args:
        page (ft.Page): 設定画面を表示する Flet ページオブジェクト。
    """
    from gui.screen.main_screen import show_main

    page.scroll = ft.ScrollMode.AUTO
    page.vertical_alignment = ft.MainAxisAlignment.START

    # ボタン
    back_button = ft.ElevatedButton(
        "戻る", on_click=lambda e: (page.clean(), show_main(page))
    )

    page.add(
        back_button,
    )
