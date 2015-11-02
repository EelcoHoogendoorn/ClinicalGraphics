

"""
Test cases to test various basic functionality of the datamodel

Unfortunately, the UI code is both a lot more nontrivial, as well as a lot harder to test
"""

example_JSON = """
[
    {
        "h0": 734,
        "h1": 2003,
        "label": "arect",
        "l0": 303,
        "l1": 1263,
        "type": "Rectangle"
    },
    {
        "c1": 969,
        "c0": 1633,
        "type": "Marker",
        "label": "amarker"
    }
]
"""

import tempfile
import os
import json

import unittest

from clinicalgraphics.datamodels import DataModel


class TestModel(unittest.TestCase):

    """
    Test case to test various aspects of the datamodel
    """
    def setUp(self):
        self.fname = tempfile.mktemp()
        with open(self.fname, 'w') as fh:
            fh.writelines(example_JSON)

    def test_io(self):
        """assert that saving the datamodel results in equivalent JSON"""
        datamodel = DataModel(None, self.fname)
        datamodel.save()

        for e, t in zip(json.loads(example_JSON), json.load(open(self.fname))):
            self.assertDictEqual(e, t, "Unable to handle annotation: "+ str(e))

    def test_select_delete(self):
        """Test selecting and deleting one of the annotations"""
        datamodel = DataModel(None, self.fname)
        annotations = datamodel.annotations
        annotation = datamodel._annotations[0]
        sa = datamodel.select(annotation.center)
        self.assertEqual(annotation, sa, "Cannot selected object by its centroid")
        datamodel.delete_selected()
        self.assertEqual(datamodel.annotations, annotations-1, "Deleting selected annotation failed")

    def tearDown(self):
        """Remove the """
        os.remove(self.fname)




