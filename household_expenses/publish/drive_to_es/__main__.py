from pkgs import client
import logging

if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s', level=logging.ERROR)

    client.run()
