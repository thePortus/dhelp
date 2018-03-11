#!/usr/bin/python

import os
import errno
import shutil
from collections import UserString, deque


class BasePath(UserString):
    """
    Used to interact with a system path in various ways. Not generally meant to
    be used directly, BasePath is parent to various Folder and File classes.

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
            >>> print(BasePath('some/extant/path').exists())
            True
            >>> print(BasePath('some/non-extant/path').exists())
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
            >>> print(BasePath(some/path.txt))
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
            >>> print(BasePath(some/path.txt))
            path.txt
        """
        return os.path.basename(self.data)

    @property
    def dirname(self):
        """Get parent directory path.

        Returns the absolute path of the parent directory of the current path.

        Returns: :obj:`str` Name of parent directory of current path

        Example:
            >>> print(BasePath(some/path.txt).dirname())
            /absolute/path/to/some

        """
        return os.path.dirname(self.data)

    @property
    def is_dir(self):
        """Check if path is a directory.

        Returns true if path points to existing directory.

        Returns: :obj:`bool` True if path points to directory, False if not

        Examples:
            >>> print(BasePath(some/path).is_dir())
            True
            >>> print(BasePath(some/path.txt).is_dir())
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
            >>> print(BasePath(some/path.txt).is_file())
            True
            >>> print(BasePath(some/path).is_file())
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
            >>> print(BasePath(some/link.txt).is_link())
            True
            >>> print(BasePath(nota/link).is_link())
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
            >>> print(BasePath('some/path').copy('some/other-path'))
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
            >>> print(BasePath(some/path).remove())
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
            >>> print(BasePath('some/path').move('some/other-path'))
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
        return self

    def makedirs(self):
        """Create any missing parent directories of current path.

        Automatically creates any parent directories of the current path
        that do not already exist. This function is used by the .save()
        method before saving to a location to avoid errors.

        Example:
            >>> BasePath(some/path).makedirs()
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
        return self


class BaseFile(BasePath):
    """Parent class for TextFile and other file related classes.

    Base parent class to all file utility objects, not meant to be used on
    its own. Child classes inherit these functions to work with specific
    file types.

    Args:
        path (:obj:`str`) System path pointing to desired file location

    Examples:
        >>> file = BaseFile('some/path')
        >>> print(folder)
        '/absolute/path/to/some/path'

        >>> # use the with..as... syntax to load, edit, and save the file
        >>> with BaseFile('some/path') as edit_file:
        ...     # any changes you make here will be automataically saved
        ...     edit_file = edit_file.replace('\n', '')
    """ # noqa

    def __enter__(self):
        return self.load()

    def __exit__(self, ctx_type, ctx_value, ctx_traceback):
        # write over previous file data
        return self.save(options={'overwrite': True})


class BaseFolder(BasePath):
    """Parent class for TextFolder and other folder related classes.

    Base parent class to all folder utility objects, not meant to be used on
    its own. Child classes inherit these functions to work with specific
    file types.

    Args:
        path (:obj:`str`) System path pointing to desired folder location

    Attributes:
        file_class (:obj:`<type 'class'>`) Class to use when constructing files
        contents (:obj:`list` of :obj:`str`) List of file and folder names
        length (:obj:`int`) Total number of items at top level insider folder
        filenames (:obj:`list` of :obj:`str`) List of only file names
        folders (:obj:`list` of `:obj:`str`) List of only subfolder names

    Methods:
        files (:obj:`list` of :obj:`self.file_class`)


    Examples:
        >>> folder = BaseFolder('some/path')
        >>> print(folder)
        '/absolute/path/to/some/path'
    """ # noqa
    file_class = BaseFile

    def __enter__(self):
        pass

    def __exit__(self, ctx_type, ctx_value, ctx_traceback):
        pass

    @property
    def contents(self):
        """Lists contents of folder.

        Returns:
            :obj:`list` of :obj:`str` File/folder names.

        Example:
            >>> print(Folder(some/path)filenames)
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
    def filenames(self):
        """Returns .contents with non-files filtered.

        Grabs names of directory contents before joining them with the current
        path to return list of absolute paths to all files in the directory.

        Returns:
            :obj:`list` of :obj:`str` File names

        Example:
            >>> print(Folder(some/path)filenames)
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

    def files(self, options={}):
        """ Load all .txt files as BaseFile objects.

        All current files inside the folder at the current path will
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
            >>> folder_files = BaseFolder('some/path').files()
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
            # add new BaseFile linked to the folder_item's location
            contents.append(
                self.file_class(os.path.join(self.data, folder_item))
            )
        # return as a deque instead of a list
        return deque(contents)
