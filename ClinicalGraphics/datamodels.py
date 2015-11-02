

"""
Data model classes
Handles organization in memory and persistence to disk,
and exposes various methods for manipulation by a view
"""

import os
import json
import dicom


from traits.api import HasTraits, Bool, Event, Instance


class DataModel(HasTraits):
    """
    Data model object for a DIMCOM dataset and its annotations
    contains a link to a dataset,
    and its in-memory representation

    Supports adding and removing annotations
    """

    _annotations = []
    selected = None

    def __init__(self, datapath, metadatapath = None):
        """
        Bind the datamodel to a DICOM file
        If a seperate metadatapath is given, this is where annotations will be read and written
        If none is given, the DICOM file path with a .json extension is used
        """
        self.datapath = datapath
        self.metadatapath = os.path.splitext(datapath)[0]+'.json' if metadatapath == None else metadatapath

        if not self.datapath is None:
            self.load_data()
        self.load_metadata()

##        self.selected = None


    def load_data(self):
        """
        Load the DICOM file
        """
        fh = dicom.read_file(self.datapath)
        self.data = fh.pixel_array

    def load_metadata(self):
        """Load the metadata, if present"""
        try:
            metadata = json.load(open( self.metadatapath))
        except:
            metadata = []
        self._annotations = [self.parse_annotation(m) for m in metadata]


    def parse_annotation(self, attrs):
        """
        Try and construct a valid annotation from an attr dict
        """
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
        Write the metadata to disk
        """
        metadata = [a.to_json() for a in self._annotations]
        json.dump(metadata, open(self.metadatapath, 'w'), indent=4)

    @property
    def shape(self):
        """The shape of the DICOM image"""
        return self.data.shape

    @property
    def annotations(self):
        """returns the total number of annotations"""
        return len(self._annotations)

    def add_annotation(self, annotation):
        """
        Add an annotation to the datamodel
        """
        self._annotations.append(annotation)

    def delete_selected(self):
        """
        Delete the annotation currently set as the selected annotation on the datamodel
        """
        if not self.selected is None:
            self._annotations.remove(self.selected)
            self.selected.removed = True
            self.selected = None

    def select(self, p):
        """
        Update selection, based on hit-testing versus the position p
        Returns the selected annotation, if any
        """
        if not self.selected is None:
            self.selected.selected = False

        for a in self._annotations:
            if a.hit_test(p):
                self.selected = a
                a.selected = True
                return a

        return None



class Annotation(HasTraits):
    """
    Annotation base class
    """
    selected = Bool(False)
    removed = Bool(False)

    def __init__(self):
        super(Annotation, self).__init__()

    def to_json():
        """
        Create a JSON represetation of the annotation
        """
        raise NotImplemented()
    def from_json():
        raise NotImplemented()
    def hit_test(self):
        """
        Perform hit-testing between the annotation and the given position p
        returns a boolean denoting hit status
        """
        raise NotImplemented()

    @property
    def center(self):
        """
        Return an (x,y) tuple representing the center
        """
        raise NotImplemented()

    @property
    def name(self):
        """A unique identifier"""
        return str(id(self))



class Rectangle(Annotation):
    """
    Bounding rectangle data model class
    """
    def __init__(self, label, l0, h0, l1, h1, **kwargs):
        super(Rectangle, self).__init__()
        self.l0, self.h0, self.l1, self.h1 = l0, h0, l1, h1
        self.label = label

    def to_json(self):
        return {
            'type':   'Rectangle',
            'label':  self.label,
            'l0':     self.l0,
            'h0':     self.h0,
            'l1':     self.l1,
            'h1':     self.h1,
        }

    def hit_test(self, p):
        p0, p1 = p
        return p0>self.l0 and p0<self.h0 and p1>self.l1 and p1<self.h1

    @property
    def center(self):
        return (self.l0+self.h0)/2, (self.l1+self.h1)/2


class Marker(Annotation):
    """
    Single point marker annotation
    """
    def __init__(self, label, c0, c1, **kwargs):
        self.c0, self.c1 = c0, c1
        self.label = label

    def to_json(self):
        return {
            'type':   'Marker',
            'label':  self.label,
            'c0':     self.c0,
            'c1':     self.c1,
        }

    def hit_test(self, p, distance = 50):
        p0, p1 = p
        return (p0-self.c0)**2+(p1-self.c1)**2 < distance**2

    @property
    def center(self):
        return self.c0, self.c1
