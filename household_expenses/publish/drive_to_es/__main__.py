from drive_to_es import client
import logging

if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s', level=logging.DEBUG)

    client.run()
