#!/usr/bin/python

""" dhelp/files/path.py

David J. Thomas

Base parent class for all file related classes, that is, all other objects in
this module. While written as an abstract class, Path() can be used directly.

"""

import os
import errno
import shutil
from collections import UserString


class Path(UserString):
    """
    Used to interact with a system path in various ways. Not generally meant to
    be used directly, Path is parent to various Folder and File classes.

    Example:
        if(Path('a_path.txt').is_file()):
            some_function()
    """

    def __init__(self, filepath=None):
        # call parent class constructor and set to a string
        super().__init__(str)
        # if no filepath specified, default to current working directory
        if not filepath:
            filepath = os.getcwd()
        # raise error if filepath sent but is non-string
        if type(filepath) is not str:
            raise Exception('filepath is not a string')
        # if relative path sent, convert to absolute path
        if not os.path.isabs(filepath):
            filepath = os.path.abspath(os.path.join(os.getcwd(), filepath))
        self.data = filepath

    @property
    def exists(self):
        """
        Check if anything exists at the filepath
        """
        return os.path.exists(self.data)

    @property
    def size(self):
        """
        Returns the size of any item at the specified path in bytes, returns
        0 if non-extant.
        """
        if not self.exists:
            return 0
        return os.path.getsize(self.data)

    @property
    def basename(self):
        """
        Returns the basename (last element of path) of the current path
        e.g. the name of the current file or folder
        """
        return os.path.basename(self.data)

    @property
    def dirname(self):
        """
        Returns the name of the parent directory of the current path
        """
        return os.path.dirname(self.data)

    @property
    def is_dir(self):
        """
        Returns true if path points to existing directory
        """
        return os.path.isdir(self.data)

    @property
    def is_file(self):
        """
        Returns true if path points to existing file
        """
        return os.path.isfile(self.data)

    @property
    def is_link(self):
        """
        Returns true if path points to symbolic link
        """
        if not self.exists:
            return False
        return os.path.islink(self.data)

    def copy(self, destination, options={}):
        """
        Copies the contents at system path (if a folder, copies it's contents
        recursively) to a specified destination. Returns a new version of the
        object linked to the new location.
        """
        # set default options
        if 'overwrite' not in options:
            options['overwrite'] = False
        # ensure is an absolute path
        if not os.path.isabs(destination):
            destination = os.path.abspath(destination)
        # if destination already exists and overwrite option not set, abort
        if os.path.exists(destination) and not options['overwrite']:
            raise Exception('Cannot copy, item exists at ' + str(destination))
        # attempt to copy location recursively
        try:
            if self.is_file:
                shutil.copy(self.data, destination)
            else:
                shutil.copytree(self.data, destination)
        # raise exception msg if error encountered
        except:
            raise Exception(
                'Error copying. Source:',
                self.data,
                'Destination',
                destination
            )
        # return new version of object that is linked to copied location
        return self.__class__(destination)

    def remove(self):
        """
        Deletes any item at the current path. If a folder deletes contents
        recursively. Returns True if successful.
        """
        try:
            if self.is_file:
                os.remove(self.data)
            else:
                shutil.rmtree(self.data)
        except:
            raise Exception('Error removing item at ' + self.data)
        return True

    def move(self, destination, options={}):
        """
        Effectively moves anything at the given path to the specified location.
        Calls .copy() with destination, then .remove() the current path, before
        finally the results of .copy().
        """
        if 'overwrite' not in options:
            options['overwrite'] = False
        new_path_obj = self.copy(destination, options=options)
        self.remove()
        return new_path_obj

    def load(self, options={'encoding': 'utf-8'}):
        """
        Called by child class load methods, stops from loading non-extant file
        """
        # set options defaults
        if 'encoding' not in options:
            options['encoding'] = 'utf-8'
        if 'silent' not in options:
            options['silent'] = False
        # print loading message if silent option not flagged
        if not options['silent']:
            print('Loading', self.data)
        if not self.exists:
            raise Exception('Cannot open item, nothing exists at' + self.data)

    def save(self, options={}):
        """
        Called by child class save methods, prevents overwrite without option
        """
        # set option defaults
        if 'encoding' not in options:
            options['encoding'] = 'utf-8'
        if 'overwrite' not in options:
            options['overwrite'] = False
        if 'silent' not in options:
            options['silent'] = False
        # print saving message if silent option not flagged
        if not options['silent']:
            print('Saving to', self.data)
        if self.exists and not options['overwrite']:
            raise Exception(
                'Item exists at ' + self.data + ' and overwrite not specified'
            )
        # create all parent directories required for save
        self.makedirs()

    def makedirs(self):
        """
        Automatically creates any parent directories of the current path
        that do not already exist.
        """
        # if parent directory is non-extant
        if not os.path.exists(os.path.dirname(self.data)):
            # attempt to make parent directories
            try:
                os.makedirs(os.path.dirname(self.data))
            # raise an error if somehow directories were created after check
            except OSError as exc:
                if exc.errno != errno.EEXist:
                    raise
