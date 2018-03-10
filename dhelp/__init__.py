#!/usr/bin/python

"""dhelp

David J. Thomas, thePortus.com, Copyright, 2018

Students often see great potential in Python for
historical analysis. But, before they see real payoff they often face too
many hurdles to overcome in the space of a single semester. dhelp is a tool
to allow students to quickly get to performing quick file operations, data
manipulations, and even text analysis.
"""

from .files import TextFile, TextFolder, CSVFile
from .web import WebPage
from .text import EnglishText, LatinText, AncientGreekText
