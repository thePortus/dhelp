#!/usr/bin/python

""" dhelp/text/text.py

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


class Text(UserString):
    """
    Base class for all Text objects. Can be used on its own to perform a number
    of operations, although it is best used with on of its language-specific
    children.
    """

    def __init__(self, text, options={}):
        """
        Calls parent init, sets default options, and stores text and options.
        """
        super().__init__(str)
        if 'encoding' not in options:
            options['encoding'] = 'utf-8'
        if 'language' not in options:
            options['language'] = 'english'
        self.data = text
        self.options = options

    def stringify(self):
        """
        Returns the text of this object as a pure string type.
        """
        return str(self.data)

    def rm_lines(self):
        """
        Gives a new version of the text with all endlines removed. Removes
        any dashed line endings and rejoins split words.
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
        """
        return self.__class__(
            "".join(re.findall("([A-Za-z ])", self.data)),
            self.options
        )

    def rm_edits(self):
        """
        Gives a new version with any text between editorial marks such as
        brackets or parentheses removed.
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

    def re_search(self, pattern):
        """
        Receives a RegEx search pattern and returns True/False if it matches.
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
        """
        word_list = list(self.tokenize())
        return pos_tag(word_list)

    def lemmatize(self):
        """
        Gives a new version of the text in which every word is lemmatized. All
        verbs are transformed into the first person singular present active,
        all nouns are transformed into the singular masculine nominative, et.c.
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

    def ngrams(self, gram_size=3):
        """
        Returns a list of ngrams, each ngram represented as a tuple
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
        """
        tokens = self.tokenize()
        return list(skipgrams(tokens, gram_size, skip_size))
