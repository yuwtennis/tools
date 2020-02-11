
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
        self._logger.setLevel(logging.DEBUG)

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

            data1 = self._parse_overview_of_software_power_consumers()
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
    def _parse_overview_of_software_power_consumers(self):

        lines      = list()
        header_str = 'Usage;Wakeups/s;GPU ops/s;Disk IO/s;GFX Wakeups/s;Category;Description;PW Estimate'
        headers    = header_str.lower().replace(' ', '_').replace('/', '_per_').split(';')

        self._logger.debug(headers)

        with open( self._csv , 'r' ) as fd:

            parse_flg = False

            for line in fd:

                line = line.strip()

                # Enable flag here if you want to parse something
                if header_str in line:

                    self._logger.debug('Start parsing')
                    parse_flg = True

                elif '____________________________________________________________________' in line:
                    self._logger.debug('End parsing')
                    parse_flg = False

                # Only stack the line when the parse flag is set true
                if parse_flg:

                    # Do not parse if the line is a header
                    if header_str in line: continue

                    columns = line.split(';')
                    self._logger.debug(columns)
                    lines.append({
                        headers[-3]: columns[-3],
                        headers[-2]: columns[-2],
                        headers[-1]: columns[-1]})

        return lines

    #
    # Parse Process Device 
    
    def _parse_device_power_report(self):
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

                    lines.append(line)

        return lines
