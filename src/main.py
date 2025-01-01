import argparse

from MILP.milp_maker import MILPMaker
from ReadExcel.excel_reader import ExcelReader
from utils.logger import setup_logger

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="シフトを作成します。")
    parser.add_argument("excel_path", help="エクセルファイルのパス")
    parser.add_argument("sheet_name", help="シート名")
    parser.add_argument("-l", "--loglevel", help="ログレベル", default="INFO")
    args = parser.parse_args()

    logger = setup_logger("shift_scheduler", args.loglevel)
    logger.info("処理を開始します。")

    reader = ExcelReader(args.excel_path)
    # 希望シフト
    availability_df = reader.read(args.sheet_name)
    # capabilities
    capabilities_df = reader.read("capabilities")

    availability = dict(availability_df.apply(lambda x: x.dropna().to_dict(), axis=1))
    # ox を True/False に変換
    availability = {
        name: {
            day: True if ox == "o" else False for day, ox in availability[name].items()
        }
        for name in availability
    }
    capabilities = dict(capabilities_df.apply(lambda x: x.dropna().to_dict(), axis=1))
    # ox を True/False に変換
    capabilities = {
        name: {
            role: True if ox == "o" else False
            for role, ox in capabilities[name].items()
        }
        for name in capabilities
    }
    logger.info("availability: %s", availability)
    logger.info("capabilities: %s", capabilities)

    maker = MILPMaker(availability, capabilities)

    # 日毎のスケジュール解決
    for day in list(availability.values())[0].keys():
        try:
            schedule = maker.solve_for_day(day)
            print(f"Day {day}:")
            for role, employee in schedule.items():
                print(f"  {role}: {employee}")
        except Exception as e:
            print(f"  {e}")
        print()

    logger.info("処理を終了します。")
