#!/usr/bin/python

""" dhelp/text/setup.py

David J. Thomas

Contains functions to automatically download necessary nltk packages and
trainer data sets.

"""

import os
from collections import UserString


class CLTKSetup(UserString):
    """
    Provides functions to automatically dicover all possible packages, check
    it against local data, and download any missing data. If you have not
    already downloaded the CLTK trainer data, you should must use this.
    """

    def __init__(self, language='latin'):
        """
        Sets the string value to the language which will be set up.
        """
        if type(language) is not str:
            raise Exception('"language" was not a string.')
        self.data = language

    @property
    def data_root(self):
        """
        Returns the absolute path pointing to the cltk data root on the
        local machine.
        """
        return os.path.expanduser('~/cltk_data')

    @property
    def dir_exists(self):
        """
        Returns True/False if there is an extant folder at root path
        """
        root_path = self.data_root
        return os.path.exists(root_path) and os.path.isdir()

    @property
    def corpora_list(self):
        """
        Gets a list of all possible corpora, downloaded from CLTK
        """
        # import cltk inline
        from cltk.corpus.utils.importer import CorpusImporter
        return CorpusImporter(self.data).list_corpora

    @property
    def missing_corpora(self):
        """
        Checks possible corpora against local corpora, returns missing corpora
        """
        pass

    def setup(self):
        """
        Finds missing corpora and then downloads missing data
        """
        from cltk.corpus.utils.importer import CorpusImporter
        corpus_importer = CorpusImporter(self.data)
        for missing_corpus in self.missing_corpora():
            print('Downloading', missing_corpus)
            try:
                corpus_importer.import_corpus(missing_corpus)
            except:
                print('Problem downloading', missing_corpus, '(skipping)')
        print('Finished downloading corpora')
