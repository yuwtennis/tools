import logging
import sys
import traceback

from economy.client import run

if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ticker_list: list = [
        '^N225',
        '^NYA',
        '^IXIC',
        '^FTSE'
    ]

    indicator_list: list = [
        'NY.GDP.MKTP.CD',
        'NY.GDP.MKTP.CN',
        'NY.GDP.MKTP.KD',
        'NY.GDP.MKTP.KN',
        'NY.GDP.MKTP.KD.ZG',
        'FP.CPI.TOTL.ZG'
    ]

    try:
        run(ticker_list, indicator_list)
    except:
        traceback.print_exc(file=sys.stdout)
