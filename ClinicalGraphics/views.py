

"""
View classes for datamodels
These mostly handle the plotting behavior of the different annotations
"""

import numpy as np
from traits.api import HasTraits, Instance, Button, Enum, Str, List, Bool, on_trait_change
from traitsui.api import Item, View, EnumEditor

from chaco.api import  \
    ArrayPlotData, Plot, jet, GridDataSource, GridMapper,  \
    DataRange2D, DataRange1D, ImageData, CMapImagePlot, DataLabel
from enable.api import ComponentEditor
import chaco.default_colormaps as dc

import datamodels


from enable.api import BaseTool, AbstractOverlay



class Rectangle(HasTraits):

    rectangle = Instance(datamodels.Rectangle)

    def __init__(self, rectangle, plot):
        super(Rectangle, self).__init__()
        self.rectangle = rectangle
        self.plot = plot

        self.add_visuals()

    def add_visuals(self):
        """
        create plot components for a rectangle view
        """
        r = self.rectangle
        points = [(r.l0, r.l1),
                  (r.h0, r.l1),
                  (r.h0, r.h1),
                  (r.l0, r.h1)]
        px, py = zip(*points)
        nx = 'px_{0}'.format(r.name)
        ny = 'py_{0}'.format(r.name)

        data = self.plot.data
        data.set_data(nx, px)
        data.set_data(ny, py)

        self.polygon = self.plot.plot(
             (nx, ny),      #need to match image conventions
              type='polygon',
              name = r.name,
              edge_width = 5,
              edge_color = 'white')[0]

        self.datalabel = DataLabel(component=self.plot, data_point=(px[3], py[3]),
                           label_position="top right", padding_bottom=10,
                           border_visible=False,
                           #bgcolor=(1, 1, 0.75, 1),
                           bgcolor="white",
                           marker_color="transparent",
                           marker_line_color="transparent",
                           show_label_coords=False,
                           #label_style='bubble',
                           marker="diamond",
                           font='modern 20',
                           label_text = self.rectangle.label)

        self.plot.overlays.append(self.datalabel)
        self.set_selection()

    @on_trait_change('rectangle.removed')
    def remove_visuals(self):
        self.plot.delplot(self.rectangle.name)
        self.plot.overlays.remove(self.datalabel)

    @on_trait_change('rectangle.changed')
    def redraw(self):
        self.remove_visuals()
        self.add_visuals()
        self.plot.request_redraw()

    @on_trait_change('rectangle.selected')
    def set_selection(self):
        if self.rectangle.selected:
            self.polygon.edge_color = (0.5,0.5,0.5,1.0)
            self.datalabel.bgcolor  = (0.5,0.5,0.5,1.0)
        else:
            self.polygon.edge_color = (1.0,1.0,1.0,1.0)
            self.datalabel.bgcolor  = (1.0,1.0,1.0,1.0)
        self.plot.request_redraw()


class Marker(HasTraits):
    marker = Instance(datamodels.Marker)

    def __init__(self, marker, plot):
        super(Marker, self).__init__()
        self.marker = marker
        self.plot = plot
        self.add_visuals()

    def add_visuals(self):
        """
        create plot components for a bounding rectangle
        """
        m = self.marker
        px, py = [[m.c0], [m.c1]]
        nx = 'px_{0}'.format(m.name)
        ny = 'py_{0}'.format(m.name)

        data = self.plot.data
        data.set_data(nx, px)
        data.set_data(ny, py)

        self.point = self.plot.plot(
             (nx, ny),      #need to match image conventions
             type='scatter',
             color = 'white',
             name = m.name)[0]

        self.datalabel = DataLabel(component=self.plot, data_point=(px[0], py[0]),
                           label_position="top", padding_bottom=10,
                           border_visible=False,
                           #bgcolor=(1, 1, 0.75, 1),
                           bgcolor="white",
                           marker_color="transparent",
                           marker_line_color="transparent",
                           show_label_coords=False,
                           #label_style='bubble',
                           marker="diamond",
                           font='modern 20',
                           label_text = self.marker.label)

        self.plot.overlays.append(self.datalabel)
        self.set_selection()

    @on_trait_change('marker.removed')
    def remove_visuals(self):
        self.plot.delplot(self.marker.name)
        self.plot.overlays.remove(self.datalabel)

    @on_trait_change('marker.changed')
    def redraw(self):
        self.remove_visuals()
        self.add_visuals()
        self.plot.request_redraw()

    @on_trait_change('marker.selected')
    def set_selection(self):
        if self.marker.selected:
            self.point.color = (0.5,0.5,0.5,1.0)
            self.datalabel.bgcolor  = (0.5,0.5,0.5,1.0)
        else:
            self.point.color = (1.0,1.0,1.0,1.0)
            self.datalabel.bgcolor  = (1.0,1.0,1.0,1.0)
        self.plot.request_redraw()
