#!/usr/bin/python

""" dhelp/files/folder.py

David J. Thomas

Contains a base class for all Folder objects. It it mostly intended as a base
class.

"""

import os

from .path import Path


class Folder(Path):
    """
    Parent class to all folder utility objects
    """

    @property
    def contents(self):
        if not self.exists or not self.is_dir:
            return None
        return os.listdir(self.data)

    @property
    def length(self):
        return len(self.contents)
