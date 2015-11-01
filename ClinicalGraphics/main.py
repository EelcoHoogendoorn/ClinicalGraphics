
"""
Application entry point


"""

import numpy as np
from traits.api import HasTraits, Instance, Button, Enum, Str, List, Bool
from traitsui.api import Item, View, EnumEditor
from chaco.api import  \
    ArrayPlotData, Plot, jet, GridDataSource, GridMapper, DataRange2D, DataRange1D, ImageData, CMapImagePlot
from enable.api import ComponentEditor
import chaco.default_colormaps as dc

from datamodel import *


from enable.api import BaseTool, AbstractOverlay


class RectangleTool(BaseTool):

    """
    Tool to add rectangle annotations
    The rectangle is spanned by the points between a mousedown and mouseup
    """

    event_state = Enum("normal", "mousedown")

    def __init__(self, plot, parent):
        super(RectangleTool, self).__init__(plot)
        self.parent = parent

    def coords(self, event):
        return map(int,  self.component.map_data((event.x, event.y)))

    def mousedown_mouse_move(self, event):
        self.end = self.coords(event)
        self.parent.text = '{0},{1} : {2},{3}'.format(*(self.start+self.end))

    def normal_left_down(self, event):
        self.event_state = "mousedown"
        self.start = self.coords(event)
        event.handled = True

    def mousedown_left_up(self, event):
        self.event_state = "normal"
        self.end = self.coords(event)

        np = LabelPrompt()
        ok = np.configure_traits(kind='modal')
        if ok:
            self.parent.add_rect(self.start, self.end, np.label)
        event.handled = True


class SelectTool(BaseTool):

    """
    Tool to select annotations
    only used for deletions right now
    but could also be extended to dragging and other operations
    """

    event_state = Enum("normal", "mousedown")

    def __init__(self, plot, parent):
        super(SelectTool, self).__init__(plot)
        self.parent = parent

    def normal_left_down(self, event):
        selected = self.parent.datamodel.selected
        if selected:
            newselected = self.parent.datamodel.select( self.coords(event))
            if selected is newselected:
                np = LabelPrompt(label=selected.label)
                ok = np.configure_traits(kind='modal')
                if ok:
                    selected.label = np.label

        event.handled = True


    def normal_left_up(self, event):
        self.parent.datamodel.select( self.coords(event))
        event.handled = True

    def coords(self, event):
        return map(int,  self.component.map_data((event.x, event.y)))


##class RectangleTool(AbstractOverlay,BaseTool):
##    '''
##    provides dynamic circle overlay on a plot: left down sets circle center,
##    left down drag draws circle, left up removes circle overlay.
##    '''
##
##    _select_on = Bool(False)
##    def __init__(self,component=None,**kwargs):
##        '''
##        initialize CircleTool as an overlay and a tool
##        '''
##        AbstractOverlay.__init__(self,component=component,**kwargs)
##        BaseTool.__init__(self,component=component,**kwargs)
##
##    def coords(self, event):
##        return map(int,  self.component.map_data((event.x, event.y)))
##
##    def normal_left_down(self,event):
##        '''
##        set selection flag to True; save circle center; CircleTool to the
##        overlays list of component (plot); discard event.
##        '''
##        self._select_on = True
##        self.start = event.x, event.y
##        self.component.overlays.append(self)
##        event.handled = True
##
##    def normal_left_up(self,event):
##        '''
##        set selection flag to False; get index of the CircleTool overlay in
##        component's overlays list; discard CircleTool overlay; redraw plot;
##        discard event.
##        '''
##        self._select_on = False
##        ixself = self.component.overlays.index(self)
##        self.component.overlays.pop(ixself)
##        self.component.request_redraw()
##        event.handled = True
##
##    def normal_mouse_move(self,event):
##        '''
##        if selection flag is True, get circle centre and current point;
##        compute radius (coordinates and radius units are screen pixels.)
##        demand redraw of plot which calls self.overlay()
##        '''
##        if not self._select_on: return
##        self.end = event.x, event.y
##        self.component.request_redraw()
##
##    def overlay(self,component,gc,view_bounds=None,mode='normal'):
##        '''
##        draw gc (Kiva Graphics Context System object) on component; define
##        gc as a circle.
##        ??? in Chaco code, with gc is used.  Why?
##        '''
##        gc.set_line_width(2)
##        gc.set_stroke_color((1,1,1))
##        gc.clip_to_rect(component.x, component.y, component.width, component.height)
##        gc.rect(*(self.start+self.end))
##        gc.stroke_path()


class LabelPrompt(HasTraits):
    """
    Simple dialog for setting a string
    """
    label = Str()


import views

class Main(HasTraits):
    """
    Main UI component

    plots the image and all attributes
    """
    plot = Instance(Plot)

    tools   = Enum("Select", "Rectangle", "Marker")
    save    = Button()
    delete  = Button()
    text    = Str()

    _annotations = List()


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
            a.add_visuals(self.plot)
        self.plot.invalidate_and_redraw()

    def _plot_default(self):
        """
        construct the default plot container
        """

        self.plotdata = ArrayPlotData(imagedata = self.datamodel.data.T)
        plot = Plot(self.plotdata)
        img_plot = plot.img_plot("imagedata", colormap=jet, origin='top left')

##        x, y = np.arange(self.datamodel.shape[0]), np.arange(self.datamodel.shape[1])
##        index = GridDataSource(xdata=x, ydata=y)
##        index_mapper = GridMapper(range=DataRange2D(index))
##        color_source = ImageData(data=self.datamodel.data)
##        color_mapper = dc.jet(DataRange1D(color_source))
##
##        plot = CMapImagePlot(
##            index = index,
##            index_mapper = index_mapper,
##            value=color_source,
##            value_mapper=color_mapper)


##        ImageData(self.datamodel.data)
##        w, h = self.datamodel.shape
##        index = GridDataSource(np.arange(w), np.arange(h))
####        index_mapper = GridMapper(range=DataRange2D(low=(0, 0),
####                                                    high=(w-1, h-1)))
##
##        index_mapper = GridMapper(range=DataRange2D(index))
##
##        image_plot = ImagePlot(
##            index=index,
##            value=image_source,
##            index_mapper=index_mapper,
##            origin='top left',
##            **PLOT_DEFAULTS
##        )


##        plot.tools.append(RectangleTool(plot, self))
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
            tool = eval(self.tools+'Tool')(self.plot, self)
            self.plot.tools.append(tool)
        except:
            pass


    def add_rect(self, start, end, label):
        """
        add a rectangle to the datamodel and to the visualization
        """
        x, y = zip(start, end)
        l0, h0 = min(x), max(x)
        l1, h1 = min(y), max(y)

        br = BoundingRectangle(label, l0, h0, l1, h1)
        self.datamodel.add_annotation(br)

        br.add_visuals(self.plot)
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
        width=500, height=600, resizable=True, title="Chaco Plot")




class Panel(HasTraits):
    """
    Sidepanel for tool selection
    """
    view = View(

    )






if __name__ == '__main__':

    datapath = r'c:\docs\001'
    datamodel = DataModel(datapath)

    main = Main(datamodel)
    main.configure_traits()


