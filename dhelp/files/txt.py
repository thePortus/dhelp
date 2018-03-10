#!/usr/bin/python

import os
from collections import deque

from ._bases import BasePath, BaseFolder


class TextFile(BasePath):
    """Load and save data quickly to path specified.

    Represents the plain text file at the path specified. Loads data
    located at given path as a string. Likewise if .save() will save string
    data at the system path send to TextFile.

    This object can be used by itself, or can be constructed automatically by
    using TextFolder.

    Args:
        path (:obj:`str`) System path pointing to desired text file location

    Attributes:
        exists (:obj:`bool`) Whether or not a file exists at the location
        size (:obj:`int`) Size of item(s) stored at current location
        basename (:obj:`str`) Name of current file
        dirname (:obj:`str`) Full path to file's parent directory

    Examples:
        >>> from dhelp import TextFile
        >>> text_file = TextFile('some/path.txt')
        >>> print(text_file)
        some/path.txt
    """

    def load(self,  options={}):
        """Opens the file data as a single string.

        Opens the file using 'utf-8' unless otherwise specified in options.
        Returns data as a string unless 'readlines' option is specified, in
        which case data is returned as a list of strings.

        Args:
            options (:obj:`dict`, optional) Options settings found at respective keywords

        Raises:
            Exception: If path does not point to a file

        Examples:
            >>> file_data = TextFile('some/path.txt').load()
            >>> print(file_data)
            Lorem ipsum dolor sit amet...
        """ # noqa
        # set option defaults
        if 'encoding' not in options:
            options['encoding'] = 'utf-8'
        if 'readlines' not in options:
            options['readlines'] = False
        super(self.__class__, self).load(options)
        if not self.is_file:
            raise Exception('Item is not a file')
        file_data = ''
        with open(self.data, 'r+', encoding=options['encoding']) as read_file:
            # if option specified, return as list of text lines
            if options['readlines']:
                file_data = read_file.readlines()
            # normally return entire data as single string
            else:
                file_data = read_file.read()
        return file_data

    def save(self, data, options={}):
        """Saves string data to file.

        Receives string data and writes it to a file. If a list is received,
        it rejoins the list with endlines before saving. If anything exists
        at the current path, an exception will be raised unless the 'overwrite'
        option it set.

        Args:
            data (:obj:`str`) Data to be saved to file, must be a single string
            options (:obj:`dict`, optional) Options settings found at respective keywords

        Examples:
            >>> # saving to a new location
            >>> saved_text_file = TextFile('some/path.txt').save('Lorem ipsum dolor sit amet...') # noqa
            >>> print(saved_text_file) # noqa
            '/absolute/path/to/some/path.txt'

            >>> # setting overwrite option
            >>> options = {'overwrite': True}
            >>> saved_text_file = saved_text_file.save('consectetur adipiscing elit', options=options)
            >>> print(saved_text_file)
            /absolute/path/to/some/path.txt
        """
        # set option defaults
        if 'encoding' not in options:
            options['encoding'] = 'utf-8'
        if 'overwrite' not in options:
            options['overwrite'] = False
        super(self.__class__, self).save(options)
        with open(self.data, 'w+', encoding=options['encoding']) as write_file:
            write_file.write(data)
        return True


class TextFolder(BaseFolder, BasePath):
    """ Load or save a folder of plaintext files as a list of strings.

    Object for interacting with a folder of plain text files. Allows quick
    discovery of filepaths and construction of relevant TextFile objects. Also
    enables batch editing of an entire directory by passing a callback.

    Args:
        path (:obj:`str`) System path pointing to desired text folder location

    Examples:
        >>> from dhelp import TextFolder
        >>> text_folder = TextFolder('some/path')
        >>> print(text_folder)
        some/path
    """

    def text_files(self, options={}):
        """ Load all .txt files as TextFile objects.

        All current .txt files inside the folder at the current path will
        be returned as a deque(list) of TextFile objects. You can set which
        file extensions will be loaded with the 'extensions' option by passing
        a list of string extensions (without the '.').

        Args:
            options (:obj:`dict`, optional) Options settings found at respective keywords

        Returns:
            :obj:`collections.deque` of `:obj:`dhelp.TextFile` TextFiles of each .txt file (or other filetype)

        Raises:
            Exception: If path does not point to folder
            TypeError: If non-list is sent as extensions option

        Examples:
            >>> folder_files = TextFolder('some/path').text_files()
            >>> for folder_file in folder_files:
            ...     print(folder_file.load())
            Lorem ipsum dolor sit amet...
        """ # noqa
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
        """ Edit and save every file in the folder by passing a function.

        Opens every file and performs a callback function sent to it. Provides
        a fast means of batch editing an entire folder of txt files. Returns
        a new TextFolder linked with the modified copy.

        The callback function should have only one argument (e.g. record_data)
        which represents the data of any given file, in string format (see
        example below). Whatever the function returns is what will be
        saved to the modified file, as long as it is a string.

        Args:
            destination (:obj:`string`) System path where you want the altered folder to be saved
            modifycb (:obj:`function`) User-defined function used to modify each record's data
            options (:obj:`dict`, optional) Options settings found at respective keywords

        Returns:
            :obj:`self.__class__` New TextFolder object tied to the modified folder

        Examples:
            >>> # define a function which alters data as you wish
            >>> def modify_record(record_data):
            >>>     record_data = record_data.replace('\\n', '')
            >>>     return record_data

            >>> # if you don't specify destination, a backup will be made
            >>> options = {'destination': 'some/other-path'}

            >>> # use TextFolder().modify, pass your function as 1st arg
            >>> text_folder = TextFolder('some/path').modify(modify_record, options=options)
            >>> print(text_folder)
            /absolute/path/to/some/path
        """ # noqa
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
