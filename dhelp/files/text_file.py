#!/usr/bin/python

""" dhelp/files/folder.py

David J. Thomas

Object for interacting with a single plain text file at the path specified
upon construction. Allows loading/saving. This object can be used by itself,
or can be constructed automatically by using TextFolder.

"""

from .path import Path


class TextFile(Path):
    """
    Load and save plain text data to/from files with TextFile. Loads data
    located at given path as a string. Likewise if .save() will save string
    data at the system path send to TextFile.

    Parameters
    ----------
    path : :obj:`str`
        System path pointing to desired text file location

    Examples
    -----
    >>> from dhelp import TextFile
    >>> text_file = TextFile('some/path.txt')
    >>> print(text_file)
    'some/path.txt'
    """

    def load(self,  options={}):
        """
        Opens file and returns contents as a single string.

        Parameters
        ----------
        options : :obj:`dict`, optional
            Options settings found at respective keywords

        Raises
        ------
        Exception
            If path does not point to a file

        Examples
        -----
        >>> file_data = TextFile('some/path.txt').load()
        >>> print(file_data)
        'Lorem ipsum dolor sit amet...'
        """
        # set option defaults
        if 'encoding' not in options:
            options['encoding'] = 'utf-8'
        super(self.__class__, self).load(options)
        if not self.is_file:
            raise Exception('Item is not a file')
        file_data = ''
        with open(self.data, 'r+', encoding=options['encoding']) as read_file:
            file_data = read_file.read()
        return file_data

    def save(self, data, options={}):
        """
        Saves string data to file, won't overwrite unless option is flagged.

        Parameters
        ----------
        data : :obj:`str`
            Data to be saved to file, must be a single string
        options : :obj:`dict`, optional
            Options settings found at respective keywords

        Examples
        -----
        # saving to a new location
        >>> saved_text_file = TextFile('some/path.txt').save('Lorem ipsum dolor sit amet...') # noqa
        >>> print(saved_text_file) # noqa
        '/absolute/path/to/some/path.txt'

        # setting overwrite option
        >>> options = {'overwrite': True}
        >>> saved_text_file = saved_text_file.save('consectetur adipiscing elit', options=options)
        >>> print(saved_text_file)
        '/absolute/path/to/some/path.txt'
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
