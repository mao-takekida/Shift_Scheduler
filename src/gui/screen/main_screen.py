import logging
import sys
from pathlib import Path

import flet as ft

from schedule_solver import main

if str(Path(__file__).parents[2]) not in sys.path:
    sys.path.append(str(Path(__file__).parents[2]))
from utils.config import load_config

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
        label = ft.Text("", size=20)
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
            sheet_name = text_field.value
            update_label(f"入力: {sheet_name}")
            loading_spinner.visible = True
            self.page.update()

            try:
                config = load_config()
                main(
                    config["excel_path"],
                    sheet_name,
                    config["num_trials"],
                    config["output_dir"],
                )
                update_label(
                    f"処理が正常に終了しました.\n\
出力: {config["output_dir"] + sheet_name + "_schedule.xlsx"}"
                )
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
