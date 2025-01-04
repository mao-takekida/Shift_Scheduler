import logging

import flet as ft

from schedule_solver import main

logger = logging.getLogger("shift_scheduler")


class MainScreen:
    @staticmethod
    def show_main(page: ft.Page) -> None:
        """
        メイン画面を表示し、シフトスケジュールの作成を行います。

        Args:
            page (ft.Page): メイン画面を表示する Flet ページオブジェクト。
        """
        # 循環参照を避けるため、ここでインポート
        from gui.screen.settings import SettingsScreen

        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        # コンポーネント初期化
        label = ft.Text("", size=30)
        text_field = ft.TextField(label="シート名を入力してください")
        loading_spinner = ft.ProgressRing(visible=False)  # ローディングスピナー

        # ヘルパー関数
        def update_label(message: str):
            label.value = message
            page.update()

        # ハンドラ: 実行ボタン
        def on_submit(_):
            if submit_button.disabled:
                return
            submit_button.disabled = True
            user_input = text_field.value
            update_label(f"入力: {user_input}")
            loading_spinner.visible = True
            page.update()

            try:
                main("data/sample_data.xlsx", user_input, 2)
            except Exception as ex:
                error_message = f"エラー: {ex}"
                update_label(error_message)
                logger.error("エラーが発生しました", exc_info=True)
            finally:
                loading_spinner.visible = False
                submit_button.disabled = False
                page.update()

        # ハンドラ: 設定画面遷移ボタン
        def go_to_settings(_):
            page.clean()
            SettingsScreen.show_settings(page)

        # ボタン定義
        submit_button = ft.ElevatedButton("実行", on_click=on_submit)
        settings_button = ft.ElevatedButton("設定画面へ", on_click=go_to_settings)

        # ページ構成
        page.add(text_field, submit_button, settings_button, loading_spinner, label)
