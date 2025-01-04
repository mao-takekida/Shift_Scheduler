import logging

import flet as ft

from schedule_solver import main

logger = logging.getLogger("shift_scheduler")


class MainScreen:
    def __init__(self, page: ft.Page):
        self.page = page

    def show_main(self) -> None:
        """
        メイン画面を表示し、シフトスケジュールの作成を行います。

        Args:
            page (ft.Page): メイン画面を表示する Flet ページオブジェクト。
        """
        self.page.clean()
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER

        # コンポーネント初期化
        label = ft.Text("", size=30)
        text_field = ft.TextField(label="シート名を入力してください")
        loading_spinner = ft.ProgressRing(visible=False)  # ローディングスピナー

        # ヘルパー関数
        def update_label(message: str):
            label.value = message
            self.page.update()

        # ハンドラ: 実行ボタン
        def on_submit(_):
            if submit_button.disabled:
                return
            submit_button.disabled = True
            user_input = text_field.value
            update_label(f"入力: {user_input}")
            loading_spinner.visible = True
            self.page.update()

            try:
                main("data/sample_data.xlsx", user_input, 2)
            except Exception as ex:
                error_message = f"エラー: {ex}"
                update_label(error_message)
                logger.error("エラーが発生しました", exc_info=True)
            finally:
                loading_spinner.visible = False
                submit_button.disabled = False
                self.page.update()

        # ハンドラ: 設定画面遷移ボタン
        def go_to_settings(_):
            # 循環参照を避けるため、ここでインポート
            from gui.screen.settings import SettingsScreen

            settings_screen = SettingsScreen(self.page)
            self.page.clean()
            settings_screen.show_settings()

        # ボタン定義
        submit_button = ft.ElevatedButton("実行", on_click=on_submit)
        settings_button = ft.ElevatedButton("設定画面へ", on_click=go_to_settings)

        # ページ構成
        self.page.add(
            text_field, submit_button, settings_button, loading_spinner, label
        )
