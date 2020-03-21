
import pandas as pd
import urllib.request as rq
from bs4 import BeautifulSoup
import subprocess

# Little script to check if the tournament is applicable
def get_list_of_candidates( url, identifier, identifier_str):

    resp = rq.urlopen(url)
    soup = BeautifulSoup(resp.read().decode('utf-8'), 'html.parser')

    if identifier == 'style':

        return soup.find_all(style=identifier_str)

def notify_to_desktop(msg):

    subprocess.run(['notify-send', '--expire-time=10000', 'トーナメント申し込み状況', msg])

def main( url, tournament, identifier='style', identifier_str='text-align: center;'):

    # Get the index number of target tournament inside html
    index = [ idx for idx, val in enumerate(get_list_of_candidates(url, identifier, identifier_str)) if tournament in val ][0]
    print('Index number of {} is {}'.format(tournament, index))

    # Check if the tournament is applicable or not
    dfs = pd.read_html(url)
    msg = 'Currently {} is {}'.format(tournament, dfs[index][5][1])

    # Notify to desktop
    notify_to_desktop(msg)

if __name__ == "__main__":

    cat_url = 'https://minamiichikawa.jp/tennis_tournament/pg408.html'
    tournament = 'アドバンス男子ダブルス'

    main( cat_url, tournament )
