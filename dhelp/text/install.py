#!/usr/bin/python

import os
from collections import UserString
import nltk


class BaseInstall(UserString):
    """Parent installer class.

    Parent class for both NLTK and CLTK installer classes. Not meant to be used
    directly.

    Parameters
    ----------
    language : :obj:`str`, optional
        Desired language for install, defaults to english

    Raises
    ------
    Exception
        If argument 'language' is non-string
    """

    def __init__(self, language=None):
        if not language:
            language = 'english'
        elif type(language) is not str:
            raise Exception('"language" was not a string.')
        self.data = language


class NLTKInstall(BaseInstall):
    """Convenience installer for NLTK packages/corpora.

    Provides functions to automatically dicover all possible packages, check
    it against local data, and download any missing data. If you have not
    already downloaded the NLTK trainer data, you should must use this.

    Parameters
    ----------
    language : :obj:`str`, optional
        Desired language for install, defaults to english

    Raises
    ------
    Exception
        If argument 'language' is non-string

    Example
    -------
    >>> from dhelp.text import NLTKInstall
    >>> NLTKInstall('english')
    'english'
    """

    @property
    def data_root(self):
        """Root of nlp data.


        Returns the absolute path pointing to the language data root on the
        local machine.

        Returns
        -------
        Absolute path to the nltk data directory

        Example
        -------
        >>> NLTKInstall().data_root
        """
        return os.path.expanduser('~/nltk_data')

    def setup(self):
        """Starts download process.

        Launches NLTK download interface, either GUI or CLI, depending on OS

        Returns
        -------
        :obj:`bool`
            True if successful
        """
        nltk.download()
        return True


class CLTKInstall(BaseInstall):
    """Convenience installer for CLTK packages/corpora.

    Provides functions to automatically dicover all possible packages, check
    it against local data, and download any missing data. If you have not
    already downloaded the CLTK trainer data, you should must use this.

    Parameters
    ----------
    language : :obj:`str`, optional
        Desired language for install, defaults to latin

    Raises
    ------
    Exception
        If argument 'language' is non-string

    Example
    -------
    >>> from dhelp.text import CLTKInstall
    >>> CLTKInstall('latin')
    'latin'
    """

    def __init__(self, language=None):
        if not language:
            language = 'latin'
        super().__init__(language=language)

    @property
    def data_root(self):
        """Root of nlp data.

        Returns the absolute path pointing to the cltk data root on the
        local machine.

        Returns
        -------
        Absolute path to the cltk data directory

        Example
        -------
        >>> CLTKInstall('latin').data_root
        """
        return os.path.expanduser('~/cltk_data')

    @property
    def corpora_list(self):
        """Lists all CLTK corpora.

        Gets a list of all possible corpora, downloaded from CLTK.

        Returns
        -------
        :obj:`list`
            List of cltk corpora for specified language

        Example
        -------
        >>> CLTKInstall('latin').corpora_list
        ['latin_text_perseus', 'latin_treebank_perseus', 'latin_text_latin_library', 'phi5', 'phi7', 'latin_proper_names_cltk', 'latin_models_cltk', 'latin_pos_lemmata_cltk', 'latin_treebank_index_thomisticus', 'latin_lexica_perseus', 'latin_training_set_sentence_cltk', 'latin_word2vec_cltk', 'latin_text_antique_digiliblt', 'latin_text_corpus_grammaticorum_latinorum', 'latin_text_poeti_ditalia'] # noqa
        """
        # import cltk inline
        from cltk.corpus.utils.importer import CorpusImporter
        return CorpusImporter(self.data).list_corpora

    def setup(self):
        """Starts download process.

        Gets list of all corpora and downloads them.

        Returns
        -------
        :obj:`bool`
            True if downloading was successful, or at least no fatal errors

        Example
        -------
        >>> CLTKInstall('latin').missing_corpora
        ['latin_text_corpus_grammaticorum_latinorum', 'latin_text_poeti_ditalia'] # noqa
        """
        from cltk.corpus.utils.importer import CorpusImporter
        corpus_importer = CorpusImporter(self.data)
        for missing_corpus in self.corpora_list:
            print('Downloading', missing_corpus)
            try:
                corpus_importer.import_corpus(missing_corpus)
            except:
                print('Problem downloading', missing_corpus, '(skipping)')
        print('Finished downloading corpora')
        return True
