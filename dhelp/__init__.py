#!/usr/bin/python

"""dhelp

David J. Thomas, thePortus.com, Copyright, 2018

Students often see great potential in Python for
historical analysis. But, before they see real payoff they often face too
many hurdles to overcome in the space of a single semester. dhelp is a tool
to allow students to quickly get to performing quick file operations, data
manipulations, and even text analysis.
"""

from .files.csv_file import CSVFile
from .files.text_file import TextFile
from .files.text_folder import TextFolder
from .web.web_page import WebPage
from .text.english import EnglishText
from .text.latin import LatinText
from .text.ancient_greek import AncientGreekText
