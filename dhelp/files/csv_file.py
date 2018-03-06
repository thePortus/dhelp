#!/usr/bin/python

import sys
import os
import csv
from collections import deque

from .path import Path
from .text_file import TextFile

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
