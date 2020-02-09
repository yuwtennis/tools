
from powertop import PowertopWrapper
import os
import pprint

def test_powertop():

    csv = 'powertop.csv'
    duration = '3'

    pt = PowertopWrapper(csv, duration)

    data = pt.exec()

    assert os.path.isfile(csv) == True
