import logging
import sys
import traceback

from stocks.client import run

if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ticker_list: list = [
        '^N225',
        '^NYA',
        '^IXIC',
        '^FTSE'
    ]

    try:
        run(ticker_list)
    except:
        traceback.print_exc(file=sys.stdout)
