
"""
Chaco tools
"""

from traits.api import HasTraits, Instance, Button, Enum, Str, List, Bool

from enable.api import BaseTool, AbstractOverlay


class LabelPrompt(HasTraits):
    """
    Simple dialog for setting a string
    """
    label = Str()


class RectangleTool(BaseTool):

    """
    Tool to add rectangle annotations
    The rectangle is spanned by the points between a mousedown and mouseup event
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

class MarkerTool(BaseTool):

    """
    Tool to add marker annotations
    Simple click registration
    """

    event_state = Enum("normal", "mousedown")

    def __init__(self, plot, parent):
        super(MarkerTool, self).__init__(plot)
        self.parent = parent

    def coords(self, event):
        return map(int,  self.component.map_data((event.x, event.y)))

    def normal_left_up(self, event):
        p = self.coords(event)

        np = LabelPrompt()
        ok = np.configure_traits(kind='modal')
        if ok:
            self.parent.add_marker(p, np.label)
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
