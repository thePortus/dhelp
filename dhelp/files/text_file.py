#!/usr/bin/python

from .path import Path


class TextFile(Path):
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
