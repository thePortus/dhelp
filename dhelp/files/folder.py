#!/usr/bin/python

import os

from .path import Path


class Folder(Path):
    """Parent class for TextFolder and other folder related classes.

    Base parent class to all folder utility objects, not meant to be used on
    its own. Child classes inherit these functions to work with specific
    file types.

    Args:
        path (:obj:`str`) System path pointing to desired folder location

    Examples:
        >>> folder = Folder('some/path')
        >>> print(folder)
        '/absolute/path/to/some/path'
    """

    @property
    def contents(self):
        """Lists contents of folder.

        Returns:
            :obj:`list` of :obj:`str` File/folder names.

        Example:
            >>> print(Folder(some/path).files)
            ['file_1.txt', 'file_2.txt', 'file_3.txt', 'subfolder_1', 'subfolder_2', 'subfolder_3']
        """ # noqa
        if not self.exists or not self.is_dir:
            return None
        return os.listdir(self.data)

    @property
    def length(self):
        """Convenience method to get the len() of the folder contents.

        Returns:
            :obj:`int` Number of items in the folder

        Example:
            >>> print(Folder('some/path').length)
            3
        """
        return len(self.contents)

    @property
    def files(self):
        """Returns .contents with non-files filtered.

        Grabs names of directory contents before joining them with the current
        path to return list of absolute paths to all files in the directory.

        Returns:
            :obj:`list` of :obj:`str` File names

        Example:
            >>> print(Folder(some/path).files)
            ['/absolute/path/to/some/path/file_1.txt', '/absolute/path/to/some/path/file_2.txt', /absolute/path/to/some/path/file_3.txt]
        """ # noqa
        dir_files = []
        for folder_item in self.contents:
            if os.path.isfile(os.path.join(self.data, folder_item)):
                dir_files.append(os.path.join(self.data, folder_item))
        return dir_files

    @property
    def folders(self):
        """Returns .contents with non-folders filtered.

        Grabs names of directory contents before joining them with the current
        path to return list of absolute paths to all folders in the directory.

        Returns:
            :obj:`list` of :obj:`str` Folder names

        Example:
            >>> print(Folder(some/path).folders)
            ['subfolder_1', 'subfolder_2', 'subfolder_3']
        """
        dir_subdirs = []
        for folder_item in self.contents:
            if os.path.isdir(os.path.join(self.data, folder_item)):
                dir_subdirs.append(os.path.join(self.data, folder_item))
        return dir_subdirs
