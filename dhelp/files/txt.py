#!/usr/bin/python

from ._bases import BaseFile, BaseFolder


class TextFile(BaseFile):
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
        >>> TextFile('some/path.txt')
        '/absolute/path/to/some/path.txt'
    """ # noqa

    def load(self, *args, **kwargs):
        """Opens the file data as a single string.

        Opens the file using 'utf-8' unless otherwise specified in options.
        Returns data as a string unless 'readlines' option is specified, in
        which case data is returned as a list of strings.

        Args:
            options (:obj:`dict`, optional) Options settings found at respective keywords

        Raises:
            Exception: If path does not point to a file

        Examples:
            >>> TextFile('some/path.txt').load()
            'Lorem ipsum dolor sit amet...'
        """ # noqa
        # get default options and update with any passed options
        options = self.options
        if 'options' in kwargs:
            if type(kwargs['options']) == dict:
                options.update(kwargs['options'])
        # print loading message if silent option not flagged
        if not options['silent']:
            print('Loading', self.data)
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

    def save(self, data, *args, **kwargs):
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
            >>> TextFile('some/path.txt').save('Lorem ipsum dolor sit amet...')
            '/absolute/path/to/some/path.txt'

            >>> # setting overwrite option
            >>> options = {'overwrite': True}
            >>> TextFile('some/path.txt').save('consectetur adipiscing elit', options=options)
            '/absolute/path/to/some/path.txt'
        """ # noqa
        # get default options and update with any passed options
        options = self.options
        if 'options' in kwargs:
            if type(kwargs['options']) == dict:
                options.update(kwargs['options'])
        # print saving message if silent option not flagged
        if not options['silent']:
            print('Saving to', self.data)
        if self.exists and options['overwrite'] is not True:
            raise Exception(
                'Item exists at ' + self.data + ' and overwrite not specified'
            )
        # create all parent directories required for save
        self.makedirs()
        with open(self.data, 'w+', encoding=options['encoding']) as write_file:
            write_file.write(data)
        return True


class TextFolder(BaseFolder):
    """ Load or save a folder of plaintext files as a list of strings.

    Object for interacting with a folder of plain text files. Allows quick
    discovery of filepaths and construction of relevant TextFile objects. Also
    enables batch editing of an entire directory by passing a callback.

    Args:
        path (:obj:`str`) System path pointing to desired text folder location

    Examples:
        >>> from dhelp import TextFolder
        >>> TextFolder('some/path')
        '/absolute/path/to/some/path'
    """
    file_class = TextFile

    def modify(self, destination, modify_cb, *args, **kwargs):
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
            >>> TextFolder('some/path').modify(modify_record, options=options)
            '/absolute/path/to/some/path'
        """ # noqa
        options = self.options
        if 'options' in kwargs:
            if type(kwargs['options']) == dict:
                options.update(kwargs['options'])
        modified_folder = self.copy(destination, options=options)
        for item_file in modified_folder.files():
            item_data = modify_cb(item_file.load(options=options))
            item_file.save(item_data, options=options)
        # return self upon success
        return modified_folder
