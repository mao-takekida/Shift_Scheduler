import json
import logging
import os
import sys

logger = logging.getLogger("shift_scheduler")


def _resource_path(relative_path: str) -> str:
    """実行可能ファイルとスクリプトの両方で動作するパスを返します。"""
    try:
        # PyInstallerで実行されている場合
        base_path = sys._MEIPASS
    except AttributeError:
        # スクリプトとして実行されている場合
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def _make_config() -> dict:
    """
    デフォルトの設定ファイルを作成します。
    """
    logger.debug("Creating default config file")
    config = {
        "excel_path": "",
    }
    return config


def load_config() -> dict:
    logger.debug("Loading config file")

    # config/config.json が存在しない場合はデフォルトの設定ファイルを作成
    if not os.path.exists(_resource_path(os.path.join("config", "config.json"))):
        config = _make_config()
        save_config(config)
        return config

    config_file_path = _resource_path(os.path.join("config", "config.json"))
    try:
        with open(config_file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError as e:
        logger.error("Config file not found: %s", e)
        raise
    except json.JSONDecodeError as e:
        logger.error("Error loading config file: %s", e)
        raise


def save_config(config: dict) -> None:
    """
    設定ファイルを保存する。
    """
    config_file_path = _resource_path(os.path.join("config", "config.json"))
    with open(config_file_path, "w") as f:
        json.dump(config, f)
