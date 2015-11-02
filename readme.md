# Clincal Graphics DICOM annotator

This utility facilitates annotating DICOM files with labeled markers, which are exported to a JSON file.

## Installation

This package has one non-conda dependency, pydicom, which can be installed with:
> pip install pydicom

Installation of the package and the rest of its dependencies can be performed using the conda build recipe found in the recipe subdirectory.

(in the git working directory)
* conda build recipe
* conda install --use-local clinicalgraphics

## Basic usage

The program can be started by running run.py, or alternatively with the following python code:

* from clinicalgraphics import run
* run(r'dicom/file/path')

This will open an editor, displaying the DICOM image and associated annotations, if any are present.

The editor supports adding two types of regions of interest; point markers and rectangles.  They can be added by selecting the corresponding tool from the toolbar, and dragging/clicking the image. Images can be selected, so that they can be relabelled or deleted. By clicking the save button, all annotations are stored in a simple JSON fileformat.