#!/usr/bin/python

""" dhelp/text/cltk_text.py

David J. Thomas

Contains parent class for language-specific CLTK objects (esp. Greek/Latin).

"""

from .basic_text import BasicText


class CLTKText(BasicText):
    """
    Parent class for Latin, Classical Greek, and other CLTK language-specific
    objects. Provides access to universal CLTK commands with child classes
    adding some methods and overriding others.
    """
    pass
