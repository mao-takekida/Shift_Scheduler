import argparse
import logging
import sys
from pathlib import Path

import flet as ft

if str(Path(__file__).parents[1]) not in sys.path:
    sys.path.append(str(Path(__file__).parents[1]))

from gui.screen.main_screen import show_main
from utils.logger import setup_logger

logger = logging.getLogger("shift_scheduler")


def main():
    def app(page: ft.Page):
        show_main(page)

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

    setup_logger("shift_scheduler", args.log_level)
    main()
    logger.debug("アプリケーションを終了します")
