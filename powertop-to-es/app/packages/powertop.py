
import logging
import shutil
import sys
import os
import subprocess
import logging
import pprint

class PowertopWrapper:
    # Shared by all instances. This will be read only.
    HEADER_STR_1 = 'Usage;Wakeups/s;GPU ops/s;Disk IO/s;GFX Wakeups/s;Category;Description;PW Estimate'
    HEADER_STR_2 = 'Usage;Device Name;PW Estimate'
    UNIT_RATE    = { 'mW': 1, 'uW': 0.001, 'W': 1000 }
    LOG_LEVEL    = logging.INFO

    def __init__(self, csv='powertop.csv', duration='3'):
        # Basic stuffs
        self._csv      = csv
        self._duration = duration

        # Init logger
        self._logger   = self._prep_logger()

    #
    # Simply execute powertop command
    #
    def exec(self):

        powertop_path = self._get_powertop_path()

        try:
            subprocess.run([
                "sudo",
                powertop_path,
                "--csv="+self._csv,
                "--time="+self._duration ])

            software = self._parse_watt(self.HEADER_STR_1)
            device   = self._parse_watt(self.HEADER_STR_2)

        finally:
            os.remove(self._csv)

        return (software, device)

    #
    # Find powertop path and exit if it does not exist
    #
    def _get_powertop_path(self):

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
    def _parse_watt(self, header_str):
        lines      = list()
        headers    = header_str.lower().replace(' ', '_').replace('/', '_per_').split(';')

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

                    # Do not parse when there are not enough columns 
                    if not len(columns) == len(headers): continue

                    # Do not parse if watt information is not included in last element
                    if not 'W' in columns[-1]: continue 
                    values = { k: v for k, v in zip(headers, columns) }

                    # This key is for aggregation in elasticsearch
                    values.update({'milli_watts': self._units_to_int(values['pw_estimate'])})
                    
                    self._logger.debug(values)
                    lines.append(values)
                    
        return lines

    # Convert string formatted unit to integer watts
    def _units_to_int(self, str_unit):

        columns = str_unit.strip().split(' ')

        return float(columns[0]) * self.UNIT_RATE[ columns[-1] ]

    # All private stuffs are below
    def _prep_logger(self):
        logger_ = logging.getLogger(__name__)
        logger_.setLevel(self.LOG_LEVEL)

        return logger_

