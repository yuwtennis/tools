from stocks.client import run

if __name__ == '__main__':

    ticker_list: list = [
        '^N225',
        '^NYA',
        '^IXIC',
        '^FTSE'
    ]
    run(ticker_list)
