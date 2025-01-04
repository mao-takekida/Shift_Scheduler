import argparse

import flet as ft

from gui.screen.main_screen import MainScreen
from utils.logger import setup_logger


def main():
    def app(page: ft.Page = None):
        main_screen = MainScreen(page)
        main_screen.show_main()

    ft.app(target=app)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="GUIアプリケーションを起動します")
    parser.add_argument(
        "-l",
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
    )
    args = parser.parse_args()

    logger = setup_logger("shift_scheduler", args.log_level)

    main()
    logger.debug("アプリケーションを終了します")
