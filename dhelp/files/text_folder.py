#!/usr/bin/python

""" dhelp/files/folder.py

David J. Thomas

Object for interacting with a folder of plain text files. Allows quick
discovery of filepaths and construction of relevant TextFile objects.

"""

import os
from collections import deque

from .folder import Folder
from .text_file import TextFile


class TextFolder(Folder):
    """
    Can load or save a folder of plaintext files as a list of strings. Also
    enables batch editing of an entire directory by passing a callback.

    Parameters
    ----------
    path : :obj:`str`
        System path pointing to desired text file location

    Examples
    -----
    >>> text_folder = TextFolder('some/path')
    >>> print(text_folder)
    'some/path'
    """

    def text_files(self, options={}):
        """
        Load all .txt (or other types) in a folder as list of TextFile objects.

        Parameters
        ----------
        options : :obj:`dict`, optional
            Options settings found at respective keywords

        Returns
        -------
        :obj:`collections.deque`
            Deque where each element is a TextFile list

        Raises
        ------
        Exception
            If path does not point to folder
        TypeError
            If non-list is sent as extensions option

        Examples
        -----
        >>> folder_files = TextFolder('some/path').text_files()
        >>> for folder_file in folder_files:
        ...     print(folder_file.load())
        'Lorem ipsum dolor sit amet...'
        """
        contents = deque([])
        # set option defaults
        if 'encoding' not in options:
            options['encoding'] = 'utf-8'
        if 'extensions' not in options:
            options['extensions'] = ['txt']
        if type(options['extensions']) is not list:
            raise TypeError('Option "extensions" must be list')
        if not self.is_dir:
            raise Exception('Item is not a folder')
        for folder_item in self.contents:
            # split the name by . and grab the last element for extension
            item_ext = folder_item.split('.')[-1]
            # only proceed if item extension is in approved list
            if item_ext in options['extensions']:
                # add new TextFile linked to the folder_item's location
                contents.append(TextFile(os.path.join(self.data, folder_item)))
        # return as a deque instead of a list
        return deque(contents)

    def modify(self, destination, modify_cb, options={}):
        """
        Opens every file and performs a callback function sent to it. Provides
        a fast means of batch editing an entire folder of txt files. Returns
        a new TextFolder linked with the modified copy.

        Parameters
        ----------
        destination : :obj:`string`
            System path where you want the altered folder to be saved
        modifycb : :obj:`function`
            User-defined function used to modify each record's data
        options : :obj:`dict`, optional
            Options settings found at respective keywords

        Returns
        -------
        :obj:`files.TextFolder`
            Gives a new TextFolder object tied to the modified folder

        Examples
        -----
        >>> # define a function which alters data as you wish
        >>> def modify_record(record_data):
        >>>     record_data = record_data.replace('\n', '')
        >>>     return record_data

        >>> # if you don't specify destination, a backup will be made
        >>> options = {'destination': 'some/other-path'}

        >>> # use TextFolder().modify, pass your function as 1st arg
        >>> text_folder = TextFolder('some/path').modify(modify_record, options=options) # noqa
        >>> print(text_folder)
        '/absolute/path/to/some/path'

        """
        # set option defaults
        if 'encoding' not in options:
            options['encoding'] = 'utf-8'
        if 'extensions' not in options:
            options['extensions'] = ['txt']
        if 'overwrite' not in options:
            options['overwrite'] = True
        if 'silent' not in options:
            options['silent'] = True
        modified_folder = self.copy(destination, options=options)
        for item_file in modified_folder.text_files():
            item_data = modify_cb(item_file.load(options=options))
            item_file.save(item_data, options=options)
        # return self upon success
        return modified_folder
