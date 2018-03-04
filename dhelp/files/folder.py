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
        """
        Lists contents of folder.

        Returns
        -------
        :obj:`list`

        Example
        -------
        >>> print(Folder(some/path).files)
        ['file_1.txt', 'file_2.txt', 'file_3.txt', 'subfolder_1', 'subfolder_2', 'subfolder_3'] # noqa
        """
        if not self.exists or not self.is_dir:
            return None
        return os.listdir(self.data)

    @property
    def files(self):
        """
        Returns .contents with non-files filtered.

        Returns
        -------
        :obj:`list`

        Example
        -------
        >>> print(Folder(some/path).files)
        ['file_1.txt', 'file_2.txt', 'file_3.txt']
        """
        dir_files = []
        for folder_item in self.contents:
            if os.path.isfile(os.path.join(self.data, folder_item)):
                dir_files.append(os.path.join(self.data, folder_item))
        return dir_files

    @property
    def folders(self):
        """
        Returns .contents with non-folders filtered.

        Returns
        -------
        :obj:`list`

        Example
        -------
        >>> print(Folder(some/path).folders)
        ['subfolder_1', 'subfolder_2', 'subfolder_3']
        """
        dir_subdirs = []
        for folder_item in self.contents:
            if os.path.isdir(os.path.join(self.data, folder_item)):
                dir_subdirs.append(os.path.join(self.data, folder_item))
        return dir_subdirs

    @property
    def length(self):
        """
        Convenience method to get the len() of the folder contents.

        Returns
        -------
        :obj:`int`

        Example
        -------
        >>> print(Folder('some/path').length)
        3
        """
        return len(self.contents)
