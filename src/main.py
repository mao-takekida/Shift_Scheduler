import argparse
from typing import Dict, List

from MILP.milp_maker import MILPMaker
from ReadExcel.excel_reader import ExcelReader
from utils.logger import setup_logger
from WriteExcel.excel_writer import ExcelWriter


def setup_parser() -> argparse.ArgumentParser:
    """引数パーサーを作成して設定する関数"""
    parser = argparse.ArgumentParser(description="シフトスケジュールを作成します。")
    parser.add_argument("excel_path", help="Excelファイルのパス")
    parser.add_argument("sheet_name", help="シート名")
    parser.add_argument("-n", "--num_trials", help="試行回数", type=int, default=1)
    parser.add_argument("-l", "--loglevel", help="ログレベル", default="INFO")
    return parser


def read_excel_data(excel_path: str, sheet_name: str, logger) -> Dict:
    """Excelファイルからデータを読み込む関数"""
    logger.info("Excelファイルからデータを読み込みます。")
    reader = ExcelReader(excel_path)
    # 希望シフトデータを読み込む
    availabilities = reader.read_availabilities(sheet_name)
    # 割り当て可能な役職データを読み込む
    capabilities = reader.read_capabilities("割り当て")
    # 社員リストを読み込む
    fulltime = reader.read_fulltime("社員リスト")
    # 重みデータを読み込む
    weights = reader.read_weights("重み")
    return {
        "availabilities": availabilities,
        "capabilities": capabilities,
        "fulltime": fulltime,
        "weights": weights,
    }


def solve_schedule(data: Dict, num_trials: int, logger) -> List:
    """MILPを使用してシフトスケジュールを解決する関数"""
    logger.info("MILPを使用してシフトスケジュールを解決します。")
    maker = MILPMaker(
        data["availabilities"], data["capabilities"], data["fulltime"], data["weights"]
    )
    schedule_list = []
    days = list(data["availabilities"].values())[0].keys()

    for day in days:
        # 各日のスケジュールを解決
        logger.debug(f"{day}のスケジュールを解決中...")
        schedules = maker.solve_for_day(day, num_trials=num_trials)
        for i, schedule in enumerate(schedules):
            # 役職の順序を整える
            schedule = {
                role: schedule[role]
                for role in data["capabilities"][list(data["availabilities"].keys())[0]]
            }
            logger.debug(f"Day {day}:{i} のスケジュール:")
            for role, employee in schedule.items():
                logger.debug(f"  {role}: {employee}")
            schedule_list.append((f"{day}:{i}", schedule))

    logger.info("スケジュールの解決が完了しました。")
    return schedule_list


def write_schedule_to_excel(
    excel_path: str, sheet_name: str, schedule_list: List, logger
):
    """解決されたスケジュールを新しいExcelファイルに書き込む関数"""
    logger.info("スケジュールをExcelファイルに書き込みます。")
    output_path = str(excel_path).replace(".xlsx", "_output.xlsx")
    ewriter = ExcelWriter(output_path, sheet_name)
    ewriter.write_schedule(schedule_list)
    logger.info(f"スケジュールを書き込んだファイル: {output_path}")


def main():
    # 引数の解析
    parser = setup_parser()
    args = parser.parse_args()

    # ロガーの設定
    logger = setup_logger("shift_scheduler", args.loglevel)
    logger.info("処理を開始します。")

    # Excelファイルからのデータ読み込み
    data = read_excel_data(args.excel_path, args.sheet_name, logger)

    # シフトスケジュールの解決
    schedule_list = solve_schedule(data, args.num_trials, logger)

    # 解決されたスケジュールをExcelファイルに書き込み
    write_schedule_to_excel(args.excel_path, args.sheet_name, schedule_list, logger)

    logger.info("処理が完了しました。")


if __name__ == "__main__":
    main()
