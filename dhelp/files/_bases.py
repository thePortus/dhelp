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
    options = {}

    def __init__(self, path=None, *args, **kwargs):
        # call parent class constructor and set to a string
        super().__init__(str)
        # raise error if path not string or set path to current dir if not set
        if path and type(path) is not str:
            raise Exception('path is not a string')
        elif not path:
            path = os.getcwd()
        # or if relative path sent, convert to absolute path
        elif not os.path.isabs(path):
            path = os.path.abspath(os.path.join(os.getcwd(), path))
        # set default options
        self.options = {
            'silent': False,
            'overwrite': False,
            'encoding': 'utf-8',
            'newline': '',
            'readlines': False,
            'delimiter': ',',
            'dialect': 'excel',
            'extensions': ['txt']
        }
        # update .options if options keyword arg passed
        if 'options' in kwargs:
            if type(kwargs['options']) == dict:
                self.options.update(kwargs['options'])
        # store path as string
        self.data = path

    def __enter__(self):
        return self.load()

    def __exit__(self, ctx_type, ctx_value, ctx_traceback):
        options = self.options
        options['overwrite'] = True
        # write over previous file data
        if type(self.save_data == str):
            return self.save(self.save_data, options=options)

    @property
    def exists(self):
        """Check if anything exists at the current path.

        Returns:
            :obj:`bool` True if anything exists at path, False if not

        Example:
            >>> BasePath('some/extant/path').exists()
            True
            >>> BasePath('some/non-extant/path').exists()
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
            >>> BasePath('some/path.txt')
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
            >>> BasePath('some/path.txt')
            'path.txt'
        """
        return os.path.basename(self.data)

    @property
    def dirname(self):
        """Get parent directory path.

        Returns the absolute path of the parent directory of the current path.

        Returns: :obj:`str` Name of parent directory of current path

        Example:
            >>> BasePath('some/path.txt').dirname()
            '/absolute/path/to/some'

        """
        return os.path.dirname(self.data)

    @property
    def is_dir(self):
        """Check if path is a directory.

        Returns true if path points to existing directory.

        Returns: :obj:`bool` True if path points to directory, False if not

        Examples:
            >>> BasePath('some/path').is_dir()
            True
            >>> BasePath('some/path.txt').is_dir()
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
            >>> BasePath('some/path.txt').is_file()
            True
            >>> BasePath('some/path').is_file()
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
            >>> BasePath('some/link.txt').is_link()
            True
            >>> BasePath('nota/link').is_link()
            False
        """
        if not self.exists:
            return False
        return os.path.islink(self.data)

    def copy(self, destination, *args, **kwargs):
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
            >>> BasePath('some/path').copy('some/other-path')
            'some/other-path'
        """ # noqa
        # get default options and update with any passed options
        options = self.options
        if 'options' in kwargs:
            if type(kwargs['options']) == dict:
                options.update(kwargs['options'])
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

    def remove(self, *args, **kwargs):
        """Delete item(s) at current path.

        Deletes any item at the current path. If a folder deletes contents
        recursively. Returns True if successful.

        Returns:
            :obj:`bool` True if successful

        Raises:
            Exception: If any issue was encountered deleting item(s) at path

        Example:
            >>> BasePath('some/path').remove()
            True
        """
        # get default options and update with any passed options
        options = self.options
        if 'options' in kwargs:
            if type(kwargs['options']) == dict:
                options.update(kwargs['options'])
        try:
            if self.is_file:
                os.remove(self.data)
            else:
                shutil.rmtree(self.data)
        except:
            raise Exception('Error removing item at ' + self.data)
        return True

    def move(self, destination, *args, **kwargs):
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
            >>> BasePath('some/path').move('some/other-path')
            'some/other-path'
        """ # noqa
        # get default options and update with any passed options
        options = self.options
        if 'options' in kwargs:
            if type(kwargs['options']) == dict:
                options.update(kwargs['options'])
        new_path_obj = self.copy(destination, options=options)
        self.remove()
        return new_path_obj

    def load(self, *args, **kwargs):
        """Loading method called by child classes.

        Called by child class load methods, stops from loading non-extant file.

        Args:
            options :obj:`dict`, optional Options settings found at respective keywords

        Raises:
            Exception: If nothing exists at path
        """ # noqa
        # get default options and update with any passed options
        options = self.options
        if 'options' in kwargs:
            if type(kwargs['options']) == dict:
                options.update(kwargs['options'])
        # print loading message if silent option not flagged
        if not options['silent']:
            print('Loading', self.data)
        if not self.exists:
            raise Exception('Cannot open item, nothing exists at' + self.data)

    def save(self, *args, **kwargs):
        """Saving method called by child classes.

        Called by child class save methods, prevents overwrite without option.

        Args:
            options :obj:`dict`, optional Options settings found at respective keywords

        Raises:
            Exception: If something exists at path and overwrite option is not set
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
        return self

    def makedirs(self, *args, **kwargs):
        """Create any missing parent directories of current path.

        Automatically creates any parent directories of the current path
        that do not already exist. This function is used by the .save()
        method before saving to a location to avoid errors.

        Example:
            >>> BasePath(some/path).makedirs()
            some/path
        """
        # get default options and update with any passed options
        options = self.options
        if 'options' in kwargs:
            if type(kwargs['options']) == dict:
                options.update(kwargs['options'])
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
    """ # noqa
    pass


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
        files (:obj:`list` of :obj:`self.file_class`) List of BaseFile objects


    Examples:
        >>> # load folder object
        >>> folder = BaseFolder('some/path')
        '/absolute/path/to/some/path'

        >>> # load files in folder as list of BaseFile objects
        >>> BaseFolder('some/path').load()
        [<class 'BaseFile'>, <class 'BaseFile'>, <class 'BaseFile'>]

        >>> # use the following context to fast-load/edit/save all files
        >>> with BaseFolder('some/path') as txt_files:
        ...     for txt_file in txt_files:
        ...         with txt_file as txt_data:
        ...             txt_file.save_data = txt_data.replace('\\n', '')
    """ # noqa
    file_class = BaseFile

    def __enter__(self):
        return self.files()

    def __exit__(self, ctx_type, ctx_value, ctx_traceback):
        pass

    @property
    def contents(self):
        """Lists contents of folder.

        Returns:
            :obj:`list` of :obj:`str` File/folder names.

        Example:
            >>> Folder('some/path').contents
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
            Folder('some/path').length
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
            >>> Folder(some/path).filenames
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
            >>> Folder(some/path).folders
            ['subfolder_1', 'subfolder_2', 'subfolder_3']
        """
        dir_subdirs = []
        for folder_item in self.contents:
            if os.path.isdir(os.path.join(self.data, folder_item)):
                dir_subdirs.append(os.path.join(self.data, folder_item))
        return dir_subdirs

    def files(self, *args, **kwargs):
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
        # get default options and update with any passed options
        options = self.options
        if 'options' in kwargs:
            if type(kwargs['options']) == dict:
                options.update(kwargs['options'])
        if type(options['extensions']) is not list:
            raise TypeError('Option "extensions" must be list')
        if not self.is_dir:
            raise Exception('Item is not a folder:', self.data)
        for folder_item in self.contents:
            # split the name by . and grab the last element for extension
            item_ext = folder_item.split('.')[-1]
            # only proceed if item extension is in approved list
            if item_ext in options['extensions']:
                # add new TextFile linked to the folder_item's location
                contents.append(
                    self.file_class(
                        os.path.join(self.data, folder_item),
                        options=options
                    )
                )
        # return as a deque instead of a list
        return deque(contents)
