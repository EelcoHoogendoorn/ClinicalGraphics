
from .main import Main
from .datamodel import DataModel

def run(datapath = None):

    if datapath is None:
        datapath = r'c:\docs\001'
    datamodel = DataModel(datapath)
    main = Main(datamodel)
    main.configure_traits()
