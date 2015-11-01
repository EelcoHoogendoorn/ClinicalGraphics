from nose.tools import *

from clinicalgraphics.datamodel import DataModel


def test_datamodel():
    datapath = None
    dm = DataModel(datapath)
    print 'test'