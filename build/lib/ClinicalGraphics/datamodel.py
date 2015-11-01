
import os
import json
import dicom
from chaco.api import DataLabel

class DataModel(object):
    """
    Data model object for a DIMCOM dataset and its annotations
    contains a link to a dataset,
    and its in-memory representation

    Supports adding and removing annotations
    """

    _annotations = []

    def __init__(self, datapath, metadatapath = None):
        self.datapath = datapath
        self.metadatapath = os.path.splitext(datapath)[0]+'.json' if metadatapath == None else metadatapath

        self.load()

        self.selected = None


    def load(self):
        """
        Load the DICOM file and the annotations
        """
        fh = dicom.read_file(self.datapath)
        self.data = fh.pixel_array

        try:
            metadata = json.load(open( self.metadatapath))
        except Exception as e:
            print e
            metadata = []


        self._annotations = [self.load_annotation(m) for m in metadata]

    def load_annotation(self, attrs):
        try:
            cls = eval(attrs['type'])
        except:
            raise Exception('Invalid annotation type')
        try:
            a = cls(**attrs)
        except:
            raise Exception('Invalid attributes {0}'.format(str(attrs)))
        return a

    def save(self):
        """
        Write the metadata to its default location
        """
        metadata = [a.to_json() for a in self._annotations]
        json.dump(metadata, open(self.metadatapath, 'w'), indent=4)

    @property
    def shape(self):
        return self.data.shape

    def add_annotation(self, annotation):
        self._annotations.append(annotation)

    def delete_selected(self):
        if not self.selected is None:
            self._annotations.remove(self.selected)
            self.selected.remove_visuals()
            self.selected = None

    @property
    def annotations(self):
        """returns the total number of annotations"""
        return len(self._annotations)

    def select(self, p):
        """
        Update selection, based on hit-testing versus the position p
        returns the selected annotation, if any
        """
        if not self.selected is None:
            self.selected.set_selection(False)

        for a in self._annotations:
            if a.hittest(p):
                self.selected = a
                a.set_selection(True)
                return a

        return None



class Annotation(object):
    """
    Annotation base class
    """
    selected = False

    def to_json():
        raise NotImplemented()
    def from_json():
        raise NotImplemented()
    def hittest(self):
        raise NotImplemented()

    @property
    def name(self):
        return str(id(self))

class BoundingRectangle(Annotation):
    """
    Bounding rectangle data model class
    """
    def __init__(self, label, l0, h0, l1, h1, **kwargs):
        self.l0, self.h0, self.l1, self.h1 = l0, h0, l1, h1
        self.label = label


    def to_json(self):
        return {
            'type':   'BoundingRectangle',
            'label':  self.label,
            'l0':     self.l0,
            'h0':     self.h0,
            'l1':     self.l1,
            'h1':     self.h1,
        }

    def hittest(self, p):
        """
        Perform hit-testing between the annotation and the given position p
        returns a boolean denoting hit status
        """
        p0, p1 = p
        return p0>self.l0 and p0<self.h0 and p1>self.l1 and p1<self.h1
##    @staticmethod
##    def from_json(attrs):
##        return BoundingRectangle(**attrs)



    def add_visuals(self, plot):
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
        self.plot = plot
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




class Marker(Annotation):
    """
    Single point marker annotation
    """
    def __init__(self, label, c0, c1, **kwargs):
        self.c0, c1 = c0, c1
        self.label = label

    def to_json(self):
        return {
            'type':   'Marker',
            'label':  self.label,
            'c0':     self.c0,
            'c1':     self.c1,
        }

##    @staticmethod
##    def from_json(attrs):
##        return Marker(**attrs)
