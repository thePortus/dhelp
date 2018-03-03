#!/usr/bin/python

""" dhelp

David J. Thomas, thePortus.com, Copyright, 2018

Helper objects for various Digital Humanities related tasks. Contains modules
to work with text files/folders, CSVs, webpages, and perform natural language
processing.

"""

from .files import CSVFile, TextFile, TextFolder
from .web import WebPage
from .text import BasicText
