#!/usr/bin/python

""" dhelp/files/csvfile.py

David J. Thomas

Contains the CSVFile object which provides helper functions to quickly save
load, and edit CSV files.

"""

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
    """
    Makes loading and saving CSV data a simple matter. Simplifies the use
    of the csv.DictReader and csv.DictWriter for loading or saving csv's as
    lists of dictionaries.
    """

    @property
    def fieldnames(self):
        """
        Opens CSV file and reads the first row to get column names.
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
        """
        Load csv as list of dictionaries.

        Example:
            loaded_data = CSVFile('a_path.csv').load()
            for data_row in loaded_data:
                print(data_row)
        """
        # set option defaults
        if 'encoding' not in options:
            options['encoding'] = 'utf-8'
        super(self.__class__, self).load(options)
        if not self.is_file:
            raise Exception('Item is not a file')
        data_rows = deque([])
        with open(
            self.data, 'r+', encoding=options['encoding'], newline=''
        ) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for csv_row in csv_reader:
                data_rows.append(csv_row)
        return data_rows

    def save(self, data, fieldnames, options={}):
        """
        Save a list of dictionaries to a .csv file. You must specify
        the column headers (fieldnames) with a list of strings. Returns True
        upon success.

        Example:
            fake_data = [
                {'id': 1, 'name': 'Sample1'},
                {'id': 2, 'name': 'Sample2'},
            ]
            fieldnames = ['id', 'name']
            CSVFile('a_path.csv').save(fake_data, fieldnames)
        """
        # calling super to set options defaults and print messages
        super(self.__class__, self).save(options)
        with open(
            self.data, 'w+', encoding=options['encoding'], newline=''
        ) as csv_file:
            csv_writer = csv.DictWriter(
                csv_file, fieldnames=fieldnames
            )
            csv_writer.writeheader()
            for data_row in data:
                csv_writer.writerow(data_row)
        return self

    def modify(self, destination, modify_cb, options={}):
        """
        Copies CSV to destination then performs the modify_cb callback
        function passed on each data row before saving the file. Quick way
        to perform batch changes to a CSV. Returns new CSVFile object linked
        to modified CSV.
        """
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
        """
        Turns text data in a csv column into a series of .txt files. Text
        is derived from a specified row (assumes 'text' if none specified).
        To use another column to generate the filename for each record, use
        filename_col, otherwise they will be numbered sequentially.
        """
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
