
"""
User intterface code

"""
import numpy as np

import datamodels
import views
import tools


from traits.api import HasTraits, Instance, Button, Enum, Str, List, Bool
from traitsui.api import Item, View, EnumEditor
from chaco.api import  \
    ArrayPlotData, Plot, jet
    #jet, GridDataSource, GridMapper, DataRange2D, DataRange1D, ImageData, CMapImagePlot
from enable.api import ComponentEditor
#import chaco.default_colormaps as dc





class Main(HasTraits):
    """
    Main UI component

    Contains the UI elements and plot containers
    """
    plot = Instance(Plot)

    tools   = Enum("Select", "Rectangle", "Marker")
    save    = Button()
    delete  = Button()
    text    = Str()

    _annotations = List()   #list of all currently active annotation views


    def __init__(self, datamodel):
        """
        Instantiate user interface
        Bind it to a datamodel by default
        """
        super(Main, self).__init__()
        self.datamodel = datamodel
        self.load_visuals()
        self._tools_changed()

    def load_visuals(self):
        """
        Create visual components for annotations which have been read from disk
        """
        for a in self.datamodel._annotations:
            if isinstance(a, datamodels.Rectangle):
                viewcls = views.Rectangle
            if isinstance(a, datamodels.Marker):
                viewcls = views.Marker
            self._annotations.append(viewcls(a, self.plot))
        self.plot.invalidate_and_redraw()

    def _plot_default(self):
        """
        Construct the default plot container, data source and image plot
        """
        self.plotdata = ArrayPlotData(imagedata = self.datamodel.data)
        plot = Plot(self.plotdata)
        img_plot = plot.img_plot("imagedata", colormap=jet, origin='top left')

        return plot

    def _tools_changed(self):
        """
        activate different tool
        """
        # Remove all tools from the plot
        plot_tools = self.plot.tools
        for tool in plot_tools:
            plot_tools.remove(tool)

        # Create new instances for the selected tool classes
        try:
            tool = eval('tools.'+self.tools+'Tool')(self.plot, self)
            self.plot.tools.append(tool)
        except:
            pass


    def add_rect(self, start, end, label):
        """
        Add a rectangle to the datamodel and to the visualization
        """
        x, y = zip(start, end)
        l0, h0 = min(x), max(x)
        l1, h1 = min(y), max(y)

        rmodel = datamodels.Rectangle(label, l0, h0, l1, h1)
        self.datamodel.add_annotation(rmodel)

        rview = views.Rectangle(rmodel, self.plot)
        self._annotations.append(rview)

        self.plot.invalidate_and_redraw()

    def add_marker(self, p, label):
        """
        Add a marker to the datamodel and to the visualization
        """
        mmodel = datamodels.Marker(label, *p)
        self.datamodel.add_annotation(mmodel)

        mview = views.Marker(mmodel, self.plot)
        self._annotations.append(mview)

        self.plot.invalidate_and_redraw()


    def _save_fired(self):
        """
        Save the datamodel to disk
        """
        try:
            self.datamodel.save()
            self.text = 'Datamodel saved'
        except Exception as e:
            self.text = str(e)

    def _delete_fired(self):
        """
        Delete the currently selected annotation from the datamodel
        Visual elements are notified by listning to the traits of the datamodel
        """
        try:
            self.datamodel.delete_selected()
            self.plot.invalidate_and_redraw()
        except Exception as e:
            print e

    traits_view = View(
        Item('plot', editor=ComponentEditor(), show_label=False),
        Item('text', show_label=False),
        Item('tools', show_label=False, style='custom'),
        Item('save', show_label=False),
        Item('delete', show_label=False),
        width=800, height=900, resizable=True, title="Annotation Editor")




class Panel(HasTraits):
    """
    Sidepanel for tool selection
    """
    view = View(

    )






if __name__ == '__main__':

    datapath = r'c:\docs\001'
    datamodel = datamodels.DataModel(datapath)

    main = Main(datamodel)
    main.configure_traits()


