import logging

import flet as ft

logger = logging.getLogger("shift_scheduler")


class SettingsScreen:
    @staticmethod
    def show_settings(page: ft.Page) -> None:
        """
        設定画面を表示し、さまざまな設定オプションを提供します。

        Args:
            page (ft.Page): 設定画面を表示する Flet ページオブジェクト。
        """
        # 循環参照を避けるため、ここでインポート
        from gui.screen.main_screen import MainScreen

        page.scroll = ft.ScrollMode.AUTO
        page.vertical_alignment = ft.MainAxisAlignment.START

        # ボタン
        back_button = ft.ElevatedButton(
            "戻る", on_click=lambda e: (page.clean(), MainScreen.show_main(page))
        )

        page.add(
            back_button,
        )
