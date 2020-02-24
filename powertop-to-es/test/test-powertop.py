import sys
import os
import pprint
sys.path.append(os.getcwd() + '/../app')

from packages.powertop import PowertopWrapper

def test_is_filedelted():
    csv = 'powertop.csv'
    duration = '3'

    pt = PowertopWrapper(csv, duration)
    data = pt.exec()

    assert os.path.isfile(csv) == False

def test_is_software_returned():
    csv = 'powertop.csv'
    duration = '3'

    pt = PowertopWrapper(csv, duration)
    data = pt.exec()

    assert len(data[0]) > 0

def test_is_device_returned():
    csv = 'powertop.csv'
    duration = '3'

    pt = PowertopWrapper(csv, duration)
    data = pt.exec()

    assert len(data[1]) > 0
