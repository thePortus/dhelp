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
    Used to load or save a single string to a single plaintext file. Will only
    overwrite existing files if passed as a property in the options dict.

    Example:
        text = 'Lorem ipsum dolor sit amet.'
        PlainTextFile('a_path.txt').load(text, options={ 'encoding': 'utf-8' })
        PlainTextFile('a_path.txt').save(text, options={ 'overwrite': True })
    """

    def load(self,  options={}):
        """
        Opens file and returns contents as a single string.
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
