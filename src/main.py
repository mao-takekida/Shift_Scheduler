import argparse

from MILP.milp_maker import MILPMaker
from ReadExcel.excel_reader import ExcelReader
from utils.logger import setup_logger
from WriteExcel.excel_writer import ExcelWriter

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
    capabilities_df = reader.read("割り当て")
    # 社員のリスト
    fulltime = reader.read_fulltime("社員リスト")

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

    # fulltime_df
    # 派遣	x
    # 齋藤	x
    # 山田	o
    # 和田	o
    # 田中	x
    # 佐藤	o
    # 中村	x
    # 小林	o
    # 加藤	x
    # 吉田	o
    # 山本	x

    # fulltime
    # 派遣 False
    # 齋藤 False
    # 山田 True
    # 和田 True
    # 田中 False
    # 佐藤 True

    logger.debug("availability: %s\n", availability)
    logger.debug("capabilities: %s\n", capabilities)
    logger.debug("fulltime: %s\n", fulltime)

    maker = MILPMaker(availability, capabilities, fulltime)

    schedule_list = []

    # 日毎のスケジュール解決
    for day in list(availability.values())[0].keys():
        schedule = maker.solve_for_day(day)
        print(f"Day {day}:")
        for role, employee in schedule.items():
            print(f"  {role}: {employee}")
        schedule_list.append(schedule)
        print()

    # ここでスケジュールをエクセルに書き込む処理を追加する
    ewriter = ExcelWriter(
        str(args.excel_path).replace(".xlsx", "_output.xlsx"), args.sheet_name
    )
    ewriter.write_schedule(list(availability.values())[0].keys(), schedule_list)

    logger.info("処理を終了します。")
