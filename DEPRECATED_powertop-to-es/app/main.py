import logging
from packages.powertop import PowertopWrapper
from packages.to_es import ToEs

def main():

  pt = PowertopWrapper()
  data = pt.exec()

  es = ToEs.get_instance()
  es.send_to_es(data[0], 'p_software')
  es.send_to_es(data[1], 'p_device')


if __name__ == '__main__':

  logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

  main()
