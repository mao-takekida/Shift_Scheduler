import logging
import sys

import colorlog

# Logger の設定
def setup_logger(logger_name: str, log_level: int) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    # フォーマットを設定（ログレベルだけ色付け）
    formatter = colorlog.ColoredFormatter(
        fmt=(
            "%(asctime)s "
            "%(log_color)s%(levelname)s%(reset)s "
            "[%(filename)s:%(lineno)d]  %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
        style="%",
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.debug("Logger set up with log level: %s", log_level)
    return logger
