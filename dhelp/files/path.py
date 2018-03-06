#!/usr/bin/python

import os
import errno
import shutil
from collections import UserString


class Path(UserString):
    """
    Used to interact with a system path in various ways. Not generally meant to
    be used directly, Path is parent to various Folder and File classes.

    Args:
        path (:obj:`str`) System path pointing to desired text file location

    Raises:
        Exception: If a non-string arg is sent as path
    """

    def __init__(self, path=None):
        # call parent class constructor and set to a string
        super().__init__(str)
        # if no filepath specified, default to current working directory
        if not path:
            path = os.getcwd()
        # raise error if path sent but is non-string
        if type(path) is not str:
            raise Exception('path is not a string')
        # if relative path sent, convert to absolute path
        if not os.path.isabs(path):
            path = os.path.abspath(os.path.join(os.getcwd(), path))
        self.data = path

    @property
    def exists(self):
        """Check if anything exists at the current path.

        Returns:
            :obj:`bool` True if anything exists at path, False if not

        Example:
            >>> print(Path('some/extant/path').exists())
            True
            >>> print(Path('some/non-extant/path').exists())
            False

        """
        return os.path.exists(self.data)

    @property
    def size(self):
        """Get file/folder size of anything at the current path.

        Returns the size of any item at the specified path in bytes, returns
        0 if non-extant.

        Returns:
            :obj:`int` Size of item at path, in bytes

        Example:
            >>> print(Path(some/path.txt))
            121
        """
        # return zero if nothing present
        if not self.exists:
            return 0
        return os.path.getsize(self.data)

    @property
    def basename(self):
        """Get file/folder name of current path.

        Returns the basename (last element of path) of the current path
        e.g. the name of the current file or folder.

        Returns:
            :obj:`str` Name of current file or folder

        Example:
            >>> print(Path(some/path.txt))
            path.txt
        """
        return os.path.basename(self.data)

    @property
    def dirname(self):
        """Get parent directory path.

        Returns the absolute path of the parent directory of the current path.

        Returns: :obj:`str` Name of parent directory of current path

        Example:
            >>> print(Path(some/path.txt).dirname())
            /absolute/path/to/some

        """
        return os.path.dirname(self.data)

    @property
    def is_dir(self):
        """Check if path is a directory.

        Returns true if path points to existing directory.

        Returns: :obj:`bool` True if path points to directory, False if not

        Examples:
            >>> print(Path(some/path).is_dir())
            True
            >>> print(Path(some/path.txt).is_dir())
            False
        """
        return os.path.isdir(self.data)

    @property
    def is_file(self):
        """Check if path is a file.

        Returns true if path points to existing file.

        Returns:
            :obj:`bool` True if path points to file, False if not

        Examples:
            >>> print(Path(some/path.txt).is_file())
            True
            >>> print(Path(some/path).is_file())
            False
        """
        return os.path.isfile(self.data)

    @property
    def is_link(self):
        """Check if path is a link.

        Returns true if path points to symbolic link.

        Returns:
            :obj:`bool` True if path points to symbolic link, False if not

        Examples:
            >>> print(Path(some/link.txt).is_link())
            True
            >>> print(Path(nota/link).is_link())
            False
        """
        if not self.exists:
            return False
        return os.path.islink(self.data)

    def copy(self, destination, options={}):
        """Copy data at path to another location.

        Copies the contents at system path (if a folder, copies it's contents
        recursively) to a specified destination. Returns a new version of the
        object linked to the new location. Will raise an error if anything
        exists at the destination unless overwrite option is flagged.

        Args:
            destination (:obj:`str`) System path to which you want to copy item(s) at current path
            options (:obj:`dict`, optional) Options settings found at respective keywords

        Returns:
            :obj:`self.__class__` New instance of object tied to the copied path

        Raises:
            Exception: If a problem is encountered when copying

        Example:
            >>> print(Path('some/path').copy('some/other-path'))
            some/other-path
        """ # noqa
        # set default options
        if 'encoding' not in options:
            options['encoding'] = 'utf-8'
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
        """Delete item(s) at current path.

        Deletes any item at the current path. If a folder deletes contents
        recursively. Returns True if successful.

        Returns:
            :obj:`bool` True if successful

        Raises:
            Exception: If any issue was encountered deleting item(s) at path

        Example:
            >>> print(Path(some/path).remove())
            True
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
        """Moves item(s) from current path to another location.

        Effectively moves anything at the given path to the specified location.
        Calls .copy() with destination, then .remove() the current path, before
        finally the results of .copy().

        Args:
            destination (:obj:`str`) System path to which you want to move item(s) at current path
            options (:obj:`dict`, optional) Options settings found at respective keywords

        Returns:
            :obj:`self.__class__` New instance of object tied to destination path

        Example:
            >>> print(Path('some/path').move('some/other-path'))
            some/other-path
        """ # noqa
        if 'encoding' not in options:
            options['encoding'] = 'utf-8'
        if 'overwrite' not in options:
            options['overwrite'] = False
        new_path_obj = self.copy(destination, options=options)
        self.remove()
        return new_path_obj

    def load(self, options={}):
        """Loading method called by child classes.

        Called by child class load methods, stops from loading non-extant file.

        Args:
            options :obj:`dict`, optional Options settings found at respective keywords

        Raises:
            Exception: If nothing exists at path
        """ # noqa
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
        """Saving method called by child classes.

        Called by child class save methods, prevents overwrite without option.

        Args:
            options :obj:`dict`, optional Options settings found at respective keywords

        Raises:
            Exception: If something exists at path and overwrite option is not set
        """ # noqa
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
        """Create any missing parent directories of current path.

        Automatically creates any parent directories of the current path
        that do not already exist. This function is used by the .save()
        method before saving to a location to avoid errors.

        Example:
            >>> Path(some/path).makedirs()
            some/path
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
