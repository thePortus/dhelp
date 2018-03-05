#!/usr/bin/python

""" dhelp/text/cltk_greek_text.py

David J. Thomas

Contains text object for using CLTK natural-language-processing on Classical
Greek-based texts. Expands on methods of parent CLTKText.

"""

from .basic_text import BasicText


class CLTKGreekText(BasicText):
    """
    Provides Classical Greek-specific CLTK functions for text passed upon
    construction. Most methods return a new version of the text, except those
    that give non-text results (e.g. pos tagging)
    """
    pass
