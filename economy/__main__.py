import json
import logging
import sys
import traceback

from economy.client import run

if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    with open("etc/config.json", 'r') as fd:
        config: dict = json.load(fd)

    try:
        run(config)
    except:
        traceback.print_exc(file=sys.stdout)
