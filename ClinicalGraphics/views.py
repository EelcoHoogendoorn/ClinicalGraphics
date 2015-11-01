

"""
User interface code
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



class RectangleView(HasTraits):

    def __init__(self, rectangle, plot):
        self.rectangle = rectangle
        self.plot = plot

    def add_visuals(self):
        """
        create plot components for a bounding rectangle
        """
        points = [(self.l0, self.l1),
                  (self.h0, self.l1),
                  (self.h0, self.h1),
                  (self.l0, self.h1)]
        px, py = zip(*points)
        nx = 'px_{0}'.format(self.name)
        ny = 'py_{0}'.format(self.name)
        data = plot.data
        data.set_data(nx, px)
        data.set_data(ny, py)

        self.polygon = plot.plot(
             (nx, ny),      #need to match image conventions
              type='polygon',
              name = self.name,
              edge_width = 5,
              edge_color = 'white')[0]

        self.datalabel = DataLabel(component=plot, data_point=(px[3], py[3]),
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
                           label_text = self.label)

        plot.overlays.append(self.datalabel)

    def remove_visuals(self):
        self.plot.delplot(self.name)
        self.plot.overlays.remove(self.datalabel)

    def redraw():
        self.remove_visuals()
        self.add_visuals()


    def set_selection(self, selected):
        if selected:
            self.polygon.edge_color = (0.5,0.5,0.5,1.0)
            self.datalabel.bgcolor  = (0.5,0.5,0.5,1.0)
        else:
            self.polygon.edge_color = (1.0,1.0,1.0,1.0)
            self.datalabel.bgcolor  = (1.0,1.0,1.0,1.0)
        self.plot.request_redraw()
