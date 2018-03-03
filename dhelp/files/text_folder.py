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
    """

    def text_files(self, options={}):
        """
        Load all .txt (or other types) in a folder as list of TextFile objects.
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
