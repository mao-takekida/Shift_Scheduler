from ReadExcel.excel_reader import ExcelReader
from utils.logger import setup_logger
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='シフトを作成します。')
    parser.add_argument('path', help='エクセルファイルのパス')
    parser.add_argument('sheet_name', help='シート名')
    parser.add_argument('-l', '--loglevel', help='ログレベル', default='INFO')
    args = parser.parse_args()
    
    logger = setup_logger('shift_scheduler', args.loglevel)
    logger.info('処理を開始します。')
    
    reader = ExcelReader(args.path)
    df = reader.read(args.sheet_name)
    logger.info(df)
    
    logger.info('処理を終了します。')
    
    
