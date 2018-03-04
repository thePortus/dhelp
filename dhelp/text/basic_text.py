#!/usr/bin/python

""" dhelp/text/basic_text.py

David J. Thomas

Contains the base object for the language-specific text objects in this module.

"""

import re
from collections import UserString

from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from nltk.util import ngrams, bigrams, trigrams, skipgrams
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag

from .install import NLTKInstall


class BasicText(UserString):
    """
    Base class for all Text objects. Can be used on its own to perform a number
    of operations, although it is best used with on of its language-specific
    children.

    Parameters
    ----------
    text : :obj:`str`
        Text to be stored for processing/nlp
    options : :obj:`dict`, optional
        Options settings found at respective keywords

    Example
    -------
    >>> from dhelp import BasicText

    >>> basic_text = BasicText('Lorem ipsum dolor sit amet...')
    >>> print(basic_text)
    'Lorem ipsum dolor sit amet...'
    """

    def __init__(self, text, options={}):
        super().__init__(str)
        if 'encoding' not in options:
            options['encoding'] = 'utf-8'
        if 'language' not in options:
            options['language'] = 'english'
        self.data = text
        self.options = options

    def setup(self):
        """
        Launches the NLTK package download interface. Overridden by the CLTK
        child classes to launch the automated CLTK downloader. Convenience
        method if user has not already downloaded NLTK packages and trainer
        sets.

        Example
        -------
        >>> BasicText('The quick brown fox jumped over the lazy dog').setup()
        """
        return NLTKInstall(self.options['language']).setup()

    def stringify(self):
        """
        Returns the text of this object as a pure string type.

        Returns
        -------
        :obj:`str`
            String form of the text

        Example
        -------
        >>> basic_text = BasicText('Lorem ipsum dolor sit amet...')
        >>> stringified_text = basic_text.stringify()
        >>> print(type(stringified_text))
        <class 'str'>
        """
        return str(self.data)

    def rm_lines(self):
        """
        Gives a new version of the text with all endlines removed. Removes
        any dashed line endings and rejoins split words.

        Returns
        -------
        self.`__class__`
            New version of text, with endlines removed

        Example
        -------
        >>> basic_text = BasicText('Lorem\nipsum do-\nlor sit amet....\n')
        >>> modified_text = basic_text.rm_lines()
        >>> print(modified_text)
        'Lorem ipsum dolor sit amet...'
        """
        rexr = re.compile(r'\n+')
        # substituting single endlines for matching endline blocks
        clean_text = rexr.sub(' ', self.data)
        return self.__class__(
            clean_text
            .replace('-\n ', '').replace('- \n', '').replace('-\n', '')
            .replace(' - ', '').replace('- ', '').replace(' -', '')
            .replace('\n', ' '),
            self.options
        )

    def rm_nonchars(self):
        """
        Gives a new version of the text with only latin characters remaining.
        Is overriden by child objects for languages using non latinate chars.

        Returns
        -------
        :obj:`self.__class__`
            Returns new version of text, with non-letters removed

        Example
        -------
        >>> basic_text = BasicText('1αLorem ipsum 2βdolor sit 3γamet...')
        >>> modified_text = basic_text.rm_nonchars()
        >>> print(modified_text)
        'Lorem ipsum dolor sit amet...'
        """
        return self.__class__(
            "".join(re.findall("([A-Za-z ])", self.data)),
            self.options
        )

    def rm_edits(self):
        """
        Gives a new version with any text between editorial marks such as
        brackets or parentheses removed.

        Returns
        -------
        :obj:`self.__class__`
            Returns new version of text, with editoria removed

        Example
        -------
        >>> basic_text = BasicText('Lore[m i]psum {dolo}r sit a(met)...')
        >>> modified_text = basic_text.rm_edits()
        >>> print(modified_text)
        'Lor psum r sit a...'
        """
        return self.__class__(
            re.sub("\〚(.*?)\〛", "", re.sub("\{(.*?)\}", "", re.sub(
                "\((.*?)\)", "", re.sub("\<(.*?)\>", "", re.sub(
                    "\[(.*?)\]", "", self.data))))),
            self.options
        )

    def rm_spaces(self):
        """
        Gives a new version of the text with extra whitespace collapsed.

        Returns
        -------
        :obj:`self.__class__`
            Returns new version of text, with extra spaced collapsed

        Example
        -------
        >>> basic_text = BasicText('Lorem   ipsum dolor  sit               amet...') # noqa
        >>> modified_text = basic_text.rm_spaces()
        >>> print(modified_text)
        'Lorem ipsum dolor sit amet...'
        """
        # regex compiler for all whitespace blocks
        rexr = re.compile(r'\s+')
        # substituting single spaces for matching whitespace blocks
        clean_text = rexr.sub(' ', self.data)
        return self.__class__(
            clean_text.strip(),
            self.options
        )

    def rm_stopwords(self, stoplist=[]):
        """
        Given a list of words or phrases, gives new text with those phrases
        removed.

        Parameters
        ----------
        stoplist : :obj:`list`
            List of words or phrases to filter from text

        Returns
        -------
        :obj:`self.__class__`
            Returns new version of text, with stop words/phrases removed

        Example
        -------
        >>> stopwords = ['ipsum', 'sit']
        >>> basic_text = BasicText('Lorem ipsum dolor sit amet...')
        >>> basic_text.rm_stopwords(stoplist=stopwords)
        >>> print(modified_text)
        'Lorem dolor amet...'
        """
        filtered_words = []
        # converts text to list of words with NLTK tokenizer
        tokenizer = PunktLanguageVars()
        tokens = tokenizer.word_tokenize(str(self.data))
        # loop through each word, if not in stoplist, append
        for word in tokens:
            not_found = True
            for stopword in stoplist:
                if str(word).strip().lower() == str(stopword).strip().lower():
                    not_found = False
            if not_found:
                filtered_words.append(word)
        # return rejoined word
        return self.__class__(
            " ".join(filtered_words),
            self.options
        )

    def lemmatize(self):
        """
        Gives a new version of the text in which every word is lemmatized. All
        verbs are transformed into the first person singular present active,
        all nouns are transformed into the singular masculine nominative, et.c.

        Returns
        -------
        :obj:`self.__class__`
            New version of the text with tokens transformed to their lemmata

        Example
        -------
        >>> basic_text = BasicText('The quick brown fox jumped over the lazy dog.') # noqa
        >>> print(basic_text.lemmatize())
        'The quick brown fox jump over the lazy dog .'
        """
        tagged_words = self.tag()
        lemmata = []
        lemmatizer = WordNetLemmatizer()
        for word, parsing in tagged_words:
            # Grab main part of speech from first character in POS
            pos = parsing[0]
            try:
                lemmatized_word = lemmatizer.lemmatize(
                    word.lower(), pos=pos.lower()[0]
                )
            except:
                lemmatized_word = word
            lemmata.append(lemmatized_word)
        return self.__class__(
            " ".join(lemmata),
            self.options
        )

    def re_search(self, pattern):
        """
        Receives a RegEx search pattern and returns True/False if it matches.

        Parameters
        ----------
        pattern: :obj:`str`
            String with the desired Regular Expression to search

        Returns
        -------
        :obj:`bool`
            True if matching, False if not

        Example
        -------
        >>> basic_text = BasicText('Lorem ipsum dolor sit amet...')
        >>> print(basic_text.re_search('Lorem ipsum'))
        True
        >>> print(basic_text.re_search('Arma virumque cano'))
        False
        """
        # Converting pattern to regex
        pattern = re.compile(pattern)
        if pattern.search(self.data):
            return True
        else:
            return False

    def tokenize(self, mode='word'):
        """
        Returns a tokenized list. By default returns list of words, but can
        also return as a list of sentences.

        Parameters
        ----------
        mode: :obj:`str`
            Specifies tokenize mode, either 'word', 'sentence', or 'wordpunct'

        Returns
        -------
        :obj:`list`
            List of (string) tokens

        Example
        -------
        >>> basic_text = BasicText('Lorem ipsum dolor sit amet. Consectetur adipiscing elit.') # noqa
        >>> print(BasicText.tokenize())
        ['Lorem', 'ipsum', 'dolor', 'sit', 'amet', '.', 'Consectetur', 'adipiscing', 'elit', '.'] # noqa
        >>> print(BasicText.tokenize(mode='sentence'))
        ['Lorem ipsum dolor sit amet.', 'Consectetur adipiscing elit.']
        """
        if mode == 'sentence':
            return (
                sent_tokenize(self.data)
            )
        elif mode == 'wordpunct':
            return wordpunct_tokenize(self.data)
        else:
            return word_tokenize(self.data)

    def tag(self):
        """
        Returns list of words marked up with parts of speech. Each word is
        returned as a 2-tuple, the first containing the word, the second with
        the parts of speech.

        Returns
        -------
        :obj:`list`
            List of words tagged as 2-tuples (word|part of speech)

        Example
        -------
        >>> basic_text = BasicText('They hated to think of sample sentences.')
        >>> basic_tags = basic_text.tag()
        >>> print(basic_tags)
        [('They', 'PRP'), ('hated', 'VBD'), ('to', 'TO'), ('think', 'VB'), ('of', 'IN'), ('sample', 'JJ'), ('sentences', 'NNS'), ('.', '.')] # noqa
        """
        word_list = list(self.tokenize())
        return pos_tag(word_list)

    def ngrams(self, gram_size=3):
        """
        Returns a list of ngrams, each ngram represented as a tuple.

        Parameters
        ----------
        gram_size : :obj:`int`, optional

        Returns
        -------
        :obj:`list`
            List of ngrams, each ngram is a tuple the length of the gram_size

        Example
        -------
        >>> basic_text = BasicText('They hated to think of sample sentences.')
        >>> basic_ngrams = basic_text.ngrams()
        >>> print(basic_ngrams)
        [('They', 'hated', 'to'), ('hated', 'to', 'think'), ('to', 'think', 'of'), ('think', 'of', 'sample'), ('of', 'sample', 'sentences'), ('sample', 'sentences', '.')] # noqa
        """
        tokens = self.tokenize()
        if gram_size < 2:   # pragma: no cover
            gram_size = 2
        if gram_size == 2:  # pragma: no cover
            return list(bigrams(tokens))
        if gram_size == 3:
            return list(trigrams(tokens))
        else:   # pragma: no cover
            return list(ngrams(tokens, gram_size))

    def skipgrams(self, gram_size=3, skip_size=1):
        """
        Returns list of skipgrams, similar to ngram, but allows spacing between
        tokens.

        Parameters
        ----------
        gram_size : :obj:`int`, optional
        skip_size : :obj:`int`, optional

        Returns
        -------
        :obj:`list`
            List of skipgrams, each ngram is a tuple the length of the gram_size

        Example
        -------
        >>> basic_text = BasicText('They hated to think of sample sentences.')
        >>> basic_skipgrams = basic_text.skipgrams()
        >>> print(basic_skipgrams)
        [('They', 'hated', 'to'), ('They', 'hated', 'think'), ('They', 'to', 'think'), ('hated', 'to', 'think'), ('hated', 'to', 'of'), ('hated', 'think', 'of'), ('to', 'think', 'of'), ('to', 'think', 'sample'), ('to', 'of', 'sample'), ('think', 'of', 'sample'), ('think', 'of', 'sentences'), ('think', 'sample', 'sentences'), ('of', 'sample', 'sentences'), ('of', 'sample', '.'), ('of', 'sentences', '.'), ('sample', 'sentences', '.')] # noqa
        """
        tokens = self.tokenize()
        return list(skipgrams(tokens, gram_size, skip_size))
