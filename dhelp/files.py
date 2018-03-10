#!/usr/bin/python

import sys
import os
import errno
import csv
import shutil
from collections import UserString, deque

# prefatory code sets csv field size to the maximum of system limit
# https://stackoverflow.com/questions/15063936/csv-error-field-larger-than-field-limit-131072
maxInt = sys.maxsize
decrement = True

while decrement:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.
    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True


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
        return self

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
        return self


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


class CSVFile(Path):
    """Load and save CSV data with lists of dictionaries.

    Makes loading and saving CSV data a simple matter. Simplifies the use
    of the csv.DictReader and csv.DictWriter for loading or saving csv's as
    lists of dictionaries.

    Args:
        path (:obj:`str`) System path pointing to desired text file location

    Examples:
        >>> from dhelp import CSVFile
        >>> csv_file = CSVFile('some/path.csv')
        >>> print(csv_file)
        some/path.csv
    """

    @property
    def fieldnames(self):
        """Get CSV column header names from the first row.

        Opens CSV file and reads the first row to get column names.

        Returns:
            :obj:`list` of :obj:`str`. Ordered CSV column headers

        Examples:
            >>> csv_file = CSVFile('some/path.csv')
            >>> print(csv_file.fieldnames)
            ['id', 'text', 'notes']
        """
        column_headers = []
        with open(self.data, 'r+') as csv_file:
            # make csv_reader and get first row from iterator with next()
            csv_reader = csv.reader(csv_file)
            header_row = next(csv_reader)
            for column_header in header_row:
                column_headers.append(column_header)
        return column_headers

    def load(self, options={}):
        """Load csv as list (deque) of dictionaries.

        Fast way to load CSV data for editing. Returns a deque, a list-like
        object. Specify alternate encoding or dialect (which affects
        how it reads quotes, et.c.) If desire, specify an alternate delimiter
        such as a semicolon, or even a tab (\t) if you want to load TSV data.

        Args:
            options (:obj:`dict`, optional) Options settings found at respective keywords

        Returns:
            :obj:`list`: List of dicts, each representing a CSV row

        Raises:
            Exception: If path does not point to file

        Examples:
            >>> csv_file = CSVFile('some/path.csv')
            >>> csv_data = CSVFile.load()
            >>> print(csv_data)
            [{'id': '1', 'text': 'Lorem ipsum', 'notes': ''}, {'id': '2', 'text': 'dolor sit', 'notes': ''}, {'id': '3', 'text': 'amet.', 'notes': ''}]
        """ # noqa
        # set option defaults
        if 'encoding' not in options:
            options['encoding'] = 'utf-8'
        if 'newline' not in options:
            options['newline'] = ''
        if 'dialect' not in options:
            options['dialect'] = 'excel'
        if 'delimiter' not in options:
            options['delimiter'] = ','
        super(self.__class__, self).load(options)
        if not self.is_file:
            raise Exception('Item is not a file')
        data_rows = deque([])
        with open(
            self.data,
            'r+',
            encoding=options['encoding'],
            newline=options['newline']
        ) as csv_file:
            csv_reader = csv.DictReader(
                csv_file,
                delimiter=options['delimiter'],
                dialect=options['dialect']
            )
            for csv_row in csv_reader:
                data_rows.append(csv_row)
        return data_rows

    def save(self, data, fieldnames, options={}):
        """Save a list of dictionaries to a .csv file.

        Send a list of dictionaries and a list of their fieldnames to save to
        the current location. You must specify the column headers (fieldnames)
        with a list of strings. You can use .fieldnames to generate these. Will
        throw exception if anything exists at current path unless 'overwrite'
        option is flagged. Returns True upon success.

        Args:
            data (:obj:`list` of :obj:`dict`) Data to save
            fieldnames (:obj:`list` of :obj:`str`) Column headers, in order
            options (:obj:`dict`, optional) Options settings found at respective keywords

        Returns:
            :obj:`self` self returned in case further operations wanted.

        Examples:
            >>> # create column names and data set
            >>> fake_fieldnames = ['id', 'text', 'notes']
            >>> fake_data = [{
            ...         'id': '1',
            ...         'text': 'Lorem ipsum',
            ...         'notes': ''
            ...     }, {
            ...         'id': '2',
            ...         'text': 'dolor sit',
            ...         'notes': ''
            ...     }, {
            ...         'id': '3',
            ...         'text': 'amet.',
            ...         'notes': ''
            ...     }]
            >>> # save to csv file
            >>> csv_file = CSVFile('some/path.csv').save(fake_data, fieldnames=fake_fieldnames)
            >>> print(csv_file)
            /absolute/path/to/some/path.csv
        """ # noqa
        if 'encoding' not in options:
            options['encoding'] = 'utf-8'
        if 'newline' not in options:
            options['newline'] = ''
        if 'dialect' not in options:
            options['dialect'] = 'excel'
        if 'delimiter' not in options:
            options['delimiter'] = ','
        # calling super to print messages
        super(self.__class__, self).save(options)
        with open(
            self.data,
            'w+',
            encoding=options['encoding'],
            newline=options['newline']
        ) as csv_file:
            csv_writer = csv.DictWriter(
                csv_file,
                fieldnames=fieldnames,
                delimiter=options['delimiter'],
                dialect=options['dialect']
            )
            csv_writer.writeheader()
            for data_row in data:
                csv_writer.writerow(data_row)
        return self

    def modify(self, destination, modify_cb, options={}):
        """Edit every row in the CSV by passing a function.

        Copies CSV to destination then performs the modify_cb callback
        function passed on each data row before saving the file. Quick way
        to perform batch changes to a CSV. Returns new CSVFile object linked
        to modified CSV.

        Args:
            destination (:obj:`str`) System path where you want the altered folder to be saved
            modifycb (:obj:`function`) User-defined function used to modify each record's data
            options (:obj:`dict`, optional) Options settings found at respective keywords

        Returns:
            :obj:`self.__class__` New CSVFile object linked to modified CSV file

        Examples:
            >>> # define a function which describes how to modify any given data row
            >>> def modify_function(csv_record):
            >>>     csv_record['text'] = 'Lorem ipsum dolor sit amet...'
            >>>     csv_record['notes'] = 'Edited with dhelp'
            >>>     return csv_record

        >>> # pass a destination and your function as arguments to .modify()
        >>> csv_file = CSVFile('some/path.csv')
        >>> altered_csv_file = csv_file.modify('some/other-path.csv', modify_cb=modify_function)

        >>> # .modify will return a new CSVFile object tied to the new location
        >>> print(altered_csv_file)
        /absolute/path/to/some/other-path.csv
        """ # noqa
        # create csv object tied to destination and empty deque for new data
        new_csv_file = self.__class__(destination)
        new_data = []
        # load data from this file, loop, perform cb function on row and append
        current_data = self.load(options=options)
        for record in current_data:
            new_data.append(modify_cb(record))
        return new_csv_file.save(
            new_data,
            fieldnames=self.fieldnames,
            options=options
        )

    def column_to_txts(
        self, destination='.', text_col='text', filename_col=None, options={}
    ):
        """Coverts a column of text data to a folder of .txt.

        Turns text data in a csv column into a series of .txt files. Text
        is derived from a specified row (assumes 'text' if none specified).
        To use another column to generate the filename for each record, use
        filename_col, otherwise they will be numbered sequentially.

        Args:
            destination (:obj:`str`) System path pointing to directory for output. Will create if doesn't exist.
            text_col (:obj:`str`, optional) CSV column name where text data is found
            filename_col (:obj:`str`, optional) CSV column name to use when generating filenames
            options (:obj:`dict`, optional) Options settings found at respective keywords

        Returns:
            :obj:`self` self returned in case further operations wanted.

        Examples:
            >>> csv_file = CSVFile('some/path.csv')
            >>> csv_file.column_to_txts('some/other-path', text_col='text', filename_col='id')
            some/path.csv
        """ # noqa
        # ensure output folder is absolute path
        if not os.path.isabs(destination):
            destination = os.path.abspath(destination)
        # load csv data, initialize counter, and loop through csv rows
        csv_data = self.load(options=options)
        counter = 0
        for record in csv_data:
            text = record[text_col]
            filepath = ''
            # determine filename, whether from column or incremental counter
            if filename_col:
                filepath = record[filename_col] + '.txt'
            else:
                filepath = str(counter) + '.txt'
            # prepend the destination directory to the filepath
            filepath = os.path.join(destination, filepath)
            # save record data to file with TextFile
            TextFile(filepath).save(text, options=options)
            counter += 1
        return self


class Folder(Path):
    """Parent class for TextFolder and other folder related classes.

    Base parent class to all folder utility objects, not meant to be used on
    its own. Child classes inherit these functions to work with specific
    file types.

    Args:
        path (:obj:`str`) System path pointing to desired folder location

    Examples:
        >>> folder = Folder('some/path')
        >>> print(folder)
        '/absolute/path/to/some/path'
    """

    @property
    def contents(self):
        """Lists contents of folder.

        Returns:
            :obj:`list` of :obj:`str` File/folder names.

        Example:
            >>> print(Folder(some/path).files)
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
    def files(self):
        """Returns .contents with non-files filtered.

        Grabs names of directory contents before joining them with the current
        path to return list of absolute paths to all files in the directory.

        Returns:
            :obj:`list` of :obj:`str` File names

        Example:
            >>> print(Folder(some/path).files)
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


class TextFolder(Folder):
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
