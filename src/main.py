import argparse

from MILP.milp_maker import MILPMaker
from ReadExcel.excel_reader import ExcelReader
from utils.logger import setup_logger
from WriteExcel.excel_writer import ExcelWriter


def main():
    parser = argparse.ArgumentParser(description="シフトを作成します。")
    parser.add_argument("excel_path", help="エクセルファイルのパス")
    parser.add_argument("sheet_name", help="シート名")
    parser.add_argument("-l", "--loglevel", help="ログレベル", default="INFO")
    args = parser.parse_args()

    logger = setup_logger("shift_scheduler", args.loglevel)
    logger.info("処理を開始します。")

    # --- read excel ---

    reader = ExcelReader(args.excel_path)
    # 希望シフト
    availabilities = reader.read_availabilities(args.sheet_name)
    # 割り当て可能な役職
    capabilities = reader.read_capabilities("割り当て")
    # 社員のリスト
    fulltime = reader.read_fulltime("社員リスト")

    # --- solve MILP ---

    maker = MILPMaker(availabilities, capabilities, fulltime)

    schedule_list = []

    # 日毎のスケジュール解決
    for day in list(availabilities.values())[0].keys():
        schedule = maker.solve_for_day(day)
        logger.info(f"Day {day}:")
        for role, employee in schedule.items():
            logger.info(f"  {role}: {employee}")
        schedule_list.append(schedule)
        logger.info("")

    # --- write excel ---

    # ここでスケジュールをエクセルに書き込む処理を追加する
    ewriter = ExcelWriter(
        str(args.excel_path).replace(".xlsx", "_output.xlsx"), args.sheet_name
    )
    ewriter.write_schedule(list(availabilities.values())[0].keys(), schedule_list)

    logger.info("処理を終了します。")


if __name__ == "__main__":
    main()
