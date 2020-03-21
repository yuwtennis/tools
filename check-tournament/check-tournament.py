
import pandas as pd
import urllib.request as rq
from bs4 import BeautifulSoup
import subprocess
import argparse
import sys

# Little script to check if the tournament is applicable
def get_list_of_candidates( url, identifier, identifier_str):

    resp = rq.urlopen(url)
    soup = BeautifulSoup(resp.read().decode('utf-8'), 'html.parser')

    if identifier == 'style':

        return soup.find_all(style=identifier_str)

def notify_to_desktop(msg):

    subprocess.run(['notify-send', '--expire-time=20000', 'トーナメント申し込み状況', msg])

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--tournament', default='アドバンス男子ダブルス')
    parser.add_argument('--url', default='https://minamiichikawa.jp/tennis_tournament/pg408.html')

    return parser.parse_args()

def main( url, tournament, identifier='style', identifier_str='text-align: center;'):

    try:

        # Get the index number of target tournament inside html
        index = [ idx for idx, val in enumerate(get_list_of_candidates(url, identifier, identifier_str)) if tournament in val ][0]
        print('Index number of {} is {}'.format(tournament, index))

        # Check if the tournament is applicable or not
        dfs = pd.read_html(url)
        msg = 'Currently {} is {}'.format(tournament, dfs[index][5][1])

        # Notify to desktop
        notify_to_desktop(msg)

    except:

        print('Something is wrong error: {}'.format(sys.exc_info()[0]))


if __name__ == "__main__":

    args = parse_args()

    main( args.url, args.tournament )
