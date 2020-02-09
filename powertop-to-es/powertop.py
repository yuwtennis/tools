import logging
import shutil
import sys
import os
import subprocess
import logging
import pprint

class PowertopWrapper:

    def __init__(self, csv, duration):

        self._csv      = csv
        self._duration = duration

        # Init logger
        logging.basicConfig(format='%(asctime)s %(message)s')
        self._logger   = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.INFO)

    #
    # Simply execute powertop command
    #
    def exec(self):

        powertop_path = self._get_path()

        try:
            subprocess.run([
                "sudo",
                powertop_path,
                "--csv="+self._csv,
                "--time="+self._duration ])

            data1 = self._parse_top10_power_consumers()
            data2 = self._parse_device_power_report()

            self._logger.info(data1)
            self._logger.info(data2)

        finally:

            os.remove(self._csv)

        return (data1, data2)

    #
    # Find powertop path and exit if it does not exist
    #
    def _get_path(self):

        path = None

        try:

            path = shutil.which('powertop')

        except shutil.Error as e:

           self._logger.error('Powertop path does not exist!')
           sys.exit(1)   

        return path

    #
    # Parse the powertop result
    #
    def _parse_top10_power_consumers(self):

        lines = list()

        with open( self._csv , 'r' ) as fd:

            parse_flg = False

            for line in fd:

                line = line.strip()

                # Enable flag here if you want to parse something
                if 'Usage;Events/s;Category;Description;PW Estimate' in line:

                    self._logger.info('Start parsing')
                    parse_flg = True

                elif '____________________________________________________________________' in line:
                    self._logger.info('End parsing')
                    parse_flg = False

                # Only stack the line if the parse flag is set true
                if parse_flg:

                    self._logger.info(line)

                    lines.append(line)

        return lines

    #
    # Parse Process Device 
    #
    def _parse_device_power_report(self):

        lines = list()

        with open( self._csv , 'r' ) as fd:

            parse_flg = False

            for line in fd:

                line = line.strip()
                if 'Usage;Device Name;PW Estimate' in line:

                    self._logger.info('Start parsing')
                    parse_flg = True

                elif '____________________________________________________________________' in line:
                    self._logger.info('End parsing')
                    parse_flg = False

                if parse_flg:


                    self._logger.info(line)

                    lines.append(line)

        return lines
