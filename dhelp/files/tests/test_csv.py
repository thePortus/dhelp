#!/usr/bin/python

import unittest

import os
import csv
import shutil

from ..csv import CSVFile


fixtures_src = os.path.join(
    os.path.dirname(__file__),
    'fixtures',
    'csv'
)
fixtures_dest = os.path.join(
    os.path.dirname(__file__),
    'fixtures',
    '.testing'
)
options = {
    'silent': False
}


class CSVFileLayer:

    @classmethod
    def testSetUp(cls):
        # remove any extant temp fixture files
        if os.path.exists(fixtures_dest):
            shutil.rmtree(fixtures_dest)
        # ensure requisite parent dirs created, make them if not
        if not os.path.exists(os.path.dirname(fixtures_dest)):
            os.makedirs(os.path.dirname(fixtures_dest))
        # copy fixture files to temp dir
        shutil.copytree(fixtures_src, fixtures_dest)

    @classmethod
    def testTearDown(cls):
        # destroy any temporary fixture files remaining
        if os.path.exists(fixtures_dest):
            shutil.rmtree(fixtures_dest)


class TestCSVFile(unittest.TestCase):
    layer = CSVFileLayer

    def test_load(self):
        # first record should match
        exempla = CSVFile(
            os.path.join(fixtures_dest, 'fake_data.csv'),
            options=options
        )
        exempla = exempla.load()[0]['text']
        comparanda = 'This is the first record'
        return self.assertEqual(exempla, comparanda)

    def test_save(self):
        # should correctly modified the first record
        csv_records = []
        # manually open csv file
        with open(
            os.path.join(
                fixtures_dest,
                'fake_data.csv'
            ),
            'r+'
        ) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for csv_record in csv_reader:
                csv_records.append(csv_record)
        # alter first record, then save to file
        csv_records[0]['text'] = 'Altered test record'
        exempla = CSVFile(
            os.path.join(fixtures_dest, 'fake_data.csv'),
            options={'overwrite': True, 'silent': False}
        )
        exempla.save(
            csv_records,
            fieldnames=['id', 'text', 'notes'],
        )
        # manually reopen csv file to check for results
        csv_records = []
        with open(
            os.path.join(
                fixtures_dest,
                'fake_data.csv'
            ),
            'r+'
        ) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for csv_record in csv_reader:
                csv_records.append(csv_record)
        return self.assertEqual(csv_records[0]['text'], 'Altered test record')

    def test_modify(self):
        # should have modified first record

        def modify_function(csv_record):
            csv_record['text'] = 'Altered test record'
            return csv_record

        exempla = CSVFile(
            os.path.join(fixtures_dest, 'fake_data.csv'),
            options={'silent': False, 'overwrite': True}
        )
        exempla.modify(
            os.path.join(fixtures_dest, 'fake_data_modified.csv'),
            modify_function
        )
        # manually reopen csv file to check for results
        csv_records = []
        with open(
            os.path.join(
                fixtures_dest,
                'fake_data_modified.csv'
            ),
            'r+'
        ) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for csv_record in csv_reader:
                csv_records.append(csv_record)
        return self.assertEqual(csv_records[4]['text'], 'Altered test record')

    def test_column_to_txts(self):
        # should produce a folder of .txt files
        exempla = ''
        comparanda = 'This is the first record'
        destination = os.path.join(
            fixtures_dest,
            'csv',
            'txt'
        )
        CSVFile(
            os.path.join(fixtures_dest, 'fake_data.csv'),
            options=options
        ).column_to_txts(
            destination=destination,
            text_col='text',
            filename_col='id',
            options={'overwrite': True}
        )
        # open file manually to check for match
        with open(
            os.path.join(fixtures_dest, 'csv', 'txt', '1.txt'),
            mode='r+'
        ) as readfile:
            exempla = readfile.read()
        return self.assertEqual(exempla, comparanda)

    def test_context_manager(self):
        exempla = CSVFile(
            os.path.join(fixtures_dest, 'fake_data.csv'),
            options=options
        )
        comparanda = 'Testing file'
        with exempla as data_rows:
            edited_rows = data_rows
            for edited_row in edited_rows:
                edited_row['text'] = 'Testing file'
            exempla.save_data = edited_rows
        # load manually to check
        with open(
            os.path.join(
                fixtures_dest,
                'fake_data.csv'
            ),
            mode='r+'
        ) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            # get value from text column of first row
            exempla = next(csv_reader)['text']
        return self.assertEqual(exempla, comparanda)
