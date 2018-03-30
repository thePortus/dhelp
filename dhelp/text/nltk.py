#!/usr/bin/python

import os

import nltk
from nltk.text import Text
from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from nltk.util import ngrams, bigrams, trigrams, skipgrams
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag

from .. import settings
from ._bases import BaseText


class NLTKMixin:
    """Mixin for NLTK-related functions.

    Mixin class which provides access to NLTK-specific functions. This class
    should be mixed with some base class (e.g. EnglishText) to give it nlp
    related functions.

    Example:
        >>> class EnglishText(NLTKTextMixin, EnglishText):
    """

    @classmethod
    def setup(self, lang_pkgs_info):
        """Download NLTK packages and trainer corpora.

        Launches the NLTK package download interface. Method is invoked by
        child .setup() methods in NLTK classes. Method is overidden in CLTK
        child classes to launch the automated CLTK downloader. Convenience
        method if user has not already downloaded NLTK packages and trainer
        sets.

        Example:
            >>> EnglishText.setup()
        """
        # start with common pkgs, a list of tuples each with...
        # (1) pkg name (2) list of path segs where pkg data is stored locally
        pkgs_and_path_segments = settings.NLTK_PACKAGES['all']
        # join common list with language specific packages
        for package_info in lang_pkgs_info:
            pkgs_and_path_segments.append(package_info)
        # loop through list of tuples, each with pkg name and path info
        for package, package_path_segments in pkgs_and_path_segments:
            # build the relative filepath to the data, specific to the os
            package_path = os.sep.join(package_path_segments)
            # will trigger error if no file, if file found, do nothing
            try:
                nltk.data.find(package_path)
                pass
            # if no file was found, download the respective package
            except:
                nltk.download(package)
        return True

    def rm_stopwords(self, stoplist=[]):
        """Removes words or phrases from the text.

        Given a list of words or phrases, gives new text with those phrases
        removed.

        Args:
            stoplist (:obj:`list`) List of words or phrases to filter from text

        Returns:
            :obj:`self.__class__` New version of text, with stop words/phrases removed

        Example:
            >>> stopwords = ['ipsum', 'sit']
            >>> text = EnglishText('Lorem ipsum dolor sit amet...')
            >>> text.rm_stopwords(stoplist=stopwords)
            >>> print(modified_text)
            'Lorem dolor amet...'
        """ # noqa
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
        """Transforms words into their lemmata.

        Gives a new version of the text in which every word is lemmatized. All
        verbs are transformed into the first person singular present active,
        all nouns are transformed into the singular masculine nominative, et.c.

        Returns:
            :obj:`self.__class__` New version of the text with tokens transformed to their lemmata

        Example:
            >>> text = EnglishText('The quick brown fox jumped over the lazy dog.')
            >>> print(text.lemmatize())
            'The quick brown fox jump over the lazy dog .'
        """ # noqa
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

    def tokenize(self, mode='word'):
        """ Splits words (or sentences) into lists of strings

        Returns a tokenized list. By default returns list of words, but can
        also return as a list of sentences.

        Args:
            mode (:obj:`str`) Specifies tokenize mode, either 'word', 'sentence', or 'wordpunct'

        Returns:
            :obj:`list` List of (string) tokens

        Example:
            >>> text = EnglishText('Lorem ipsum dolor sit amet. Consectetur adipiscing elit.') # noqa
            >>> print(EnglishText.tokenize())
            ['Lorem', 'ipsum', 'dolor', 'sit', 'amet', '.', 'Consectetur', 'adipiscing', 'elit', '.']
            >>> print(EnglishText.tokenize(mode='sentence'))
            ['Lorem ipsum dolor sit amet.', 'Consectetur adipiscing elit.']
        """ # noqa
        if mode == 'sentence':
            return (
                sent_tokenize(self.data)
            )
        elif mode == 'wordpunct':
            return wordpunct_tokenize(self.data)
        else:
            return word_tokenize(self.data)

    def tag(self):
        """Performs part-of-speech analysis on the text.

        Returns list of words marked up with parts of speech. Each word is
        returned as a 2-tuple, the first containing the word, the second with
        the parts of speech.

        Returns:
            (:obj:`list`) Words tagged as 2-tuples (word|part of speech)

        Example:
            >>> text = EnglishText('They hated to think of sample sentences.')
            >>> basic_tags = text.tag()
            >>> print(basic_tags)
            [('They', 'PRP'), ('hated', 'VBD'), ('to', 'TO'), ('think', 'VB'), ('of', 'IN'), ('sample', 'JJ'), ('sentences', 'NNS'), ('.', '.')]
        """ # noqa
        word_list = list(self.tokenize())
        return pos_tag(word_list)

    def ngrams(self, gram_size=3):
        """Gives ngrams.

        Returns a list of ngrams, each ngram represented as a tuple.

        Args:
            gram_size (:obj:`int`, optional) Size of the ngrams to generate

        Returns:
            :obj:`list` of :obj:`tuple` Words of each ngram

        Example:
            >>> text = EnglishText('They hated to think of sample sentences.')
            >>> basic_ngrams = text.ngrams()
            >>> print(basic_ngrams)
            [('They', 'hated', 'to'), ('hated', 'to', 'think'), ('to', 'think', 'of'), ('think', 'of', 'sample'), ('of', 'sample', 'sentences'), ('sample', 'sentences', '.')]
        """ # noqa
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
        """Gives skipgrams.

        Returns list of skipgrams, similar to ngram, but allows spacing between
        tokens.

        Args:
            gram_size (:obj:`int`, optional) Size of the ngrams to generate
            skip_size (:obj:`int`, optional) Size of max spacing allowed

        Returns:
            :obj:`list` of :obj:`tuple` Words of each skipgram

        Example:
            >>> text = EnglishText('They hated to think of sample sentences.')
            >>> basic_skipgrams = text.skipgrams()
            >>> print(basic_skipgrams)
            [('They', 'hated', 'to'), ('They', 'hated', 'think'), ('They', 'to', 'think'), ('hated', 'to', 'think'), ('hated', 'to', 'of'), ('hated', 'think', 'of'), ('to', 'think', 'of'), ('to', 'think', 'sample'), ('to', 'of', 'sample'), ('think', 'of', 'sample'), ('think', 'of', 'sentences'), ('think', 'sample', 'sentences'), ('of', 'sample', 'sentences'), ('of', 'sample', '.'), ('of', 'sentences', '.'), ('sample', 'sentences', '.')] # noqa
        """
        tokens = self.tokenize()
        return list(skipgrams(tokens, gram_size, skip_size))

    def word_count(self, word=None):
        """Returns counter dictionary with word counts at respective keywords.

        Performs word counts and then stores their values in the respective
        keyword of a counter dictionary. If a word is passed, a simple integer
        count of the number of appearances is returned.

        Args:
            word (:obj:`string`, optional) A single word you want to count

        Returns:
            :obj:`dict` A dictionary with word counts stored in respective keywords

        Example:
            >>> # TODO:
        """ # noqa
        counts = dict(Text(self.tokenize()).vocab())
        # If a single word was specified, only return that frequency
        if word:
            return counts[word]
        return counts


class EnglishText(NLTKMixin, BaseText):
    """Main class to interact with English-language texts.

    EnglishText provides methods for altering texts for pre-processing as well
    as numerous nlp methods for analyzing the text. Text alteration methods
    can be chained since they each return a new instance of the class created
    with the altered text.

    Args:
        text (:obj:`str`) Main text data
        options (:obj:`dict`, optional) keyword/value dict for optional settings

    Attributes:
        data (:obj:`str`) Main text data
        options (:obj:`dict`, optional) keyword/value dict for optional settings

    Methods:

    Example:
        >>> english_text = EnglishText('Th3e Qui\\nck b     rown fox jumped over the lazy dog')
        >>> english_text.rm_lines().rm_nonchars().rm_spaces()
        The quick brown fox jumped over the lazy dog
    """ # noqa

    def __init__(self, text, options={}):
        options['language'] = 'english'
        super().__init__(text=text, options=options)

    @classmethod
    def setup(self):
        # invoke parent setup method, sending it the pkg info for specific lang
        super(self.__class__).setup(settings.NLTK_PACKAGES['english'])
