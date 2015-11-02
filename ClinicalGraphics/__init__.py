


backend = 'qt4'
if backend == 'qt4':
    import os
    os.environ['ETS_TOOLKIT'] = 'qt4'


def run(datapath = None, metadatapath = None):


    from .gui import Main
    from .datamodels import DataModel

    if datapath is None:
        datapath = r'c:\docs\001'
    datamodel = DataModel(datapath, metadatapath)
    main = Main(datamodel)
    main.configure_traits()
