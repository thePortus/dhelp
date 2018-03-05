#!/usr/bin/python

from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from nltk.util import ngrams, bigrams, trigrams, skipgrams
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag

from .install import NLTKInstall


class NLTKMixin:
    """Mixin for NLTK-related functions.

    Mixin class which provides access to NLTK-specific functions. This class
    should be mixed with some base class (e.g. BaseText) to give it nlp
    related functions.

    Example:
        >>> class EnglishText(NLTKTextMixin, BaseText):
    """

    def setup(self):
        """Download NLTK packages and trainer corpora.

        Launches the NLTK package download interface. Overridden by the CLTK
        child classes to launch the automated CLTK downloader. Convenience
        method if user has not already downloaded NLTK packages and trainer
        sets.

        Example:
            >>> BaseText('The quick brown fox jumped over the lazy dog').setup() # noqa
        """
        return NLTKInstall(self.options['language']).setup()

    def rm_stopwords(self, stoplist=[]):
        """Removes words or phrases from the text.

        Given a list of words or phrases, gives new text with those phrases
        removed.

        Args:
            stoplist : :obj:`list`
                List of words or phrases to filter from text

        Returns:
            :obj:`self.__class__`
                Returns new version of text, with stop words/phrases removed

        Example:
            >>> stopwords = ['ipsum', 'sit']
            >>> base_text = BaseText('Lorem ipsum dolor sit amet...')
            >>> base_text.rm_stopwords(stoplist=stopwords)
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
        """Transforms words into their lemmata.

        Gives a new version of the text in which every word is lemmatized. All
        verbs are transformed into the first person singular present active,
        all nouns are transformed into the singular masculine nominative, et.c.

        Returns:
            :obj:`self.__class__`
                New version of the text with tokens transformed to their lemmata

        Example:
            >>> base_text = BaseText('The quick brown fox jumped over the lazy dog.') # noqa
            >>> print(base_text.lemmatize())
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

    def tokenize(self, mode='word'):
        """ Splits words (or sentences) into lists of strings

        Returns a tokenized list. By default returns list of words, but can
        also return as a list of sentences.

        Args:
            mode: :obj:`str`
                Specifies tokenize mode, either 'word', 'sentence', or 'wordpunct'

        Returns:
            :obj:`list`
                List of (string) tokens

        Example:
            >>> base_text = BaseText('Lorem ipsum dolor sit amet. Consectetur adipiscing elit.') # noqa
            >>> print(BaseText.tokenize())
            ['Lorem', 'ipsum', 'dolor', 'sit', 'amet', '.', 'Consectetur', 'adipiscing', 'elit', '.'] # noqa
            >>> print(BaseText.tokenize(mode='sentence'))
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
        """Performs part-of-speech analysis on the text.

        Returns list of words marked up with parts of speech. Each word is
        returned as a 2-tuple, the first containing the word, the second with
        the parts of speech.

        Returns:
            :obj:`list`
                List of words tagged as 2-tuples (word|part of speech)

        Example:
            >>> base_text = BaseText('They hated to think of sample sentences.')
            >>> basic_tags = base_text.tag()
            >>> print(basic_tags)
            [('They', 'PRP'), ('hated', 'VBD'), ('to', 'TO'), ('think', 'VB'), ('of', 'IN'), ('sample', 'JJ'), ('sentences', 'NNS'), ('.', '.')] # noqa
        """
        word_list = list(self.tokenize())
        return pos_tag(word_list)

    def ngrams(self, gram_size=3):
        """Gives ngrams.

        Returns a list of ngrams, each ngram represented as a tuple.

        Args:
            gram_size : :obj:`int`, optional

        Returns:
            :obj:`list`
                List of ngrams, each ngram is a tuple the length of the gram_size

        Example:
            >>> base_text = BaseText('They hated to think of sample sentences.')
            >>> basic_ngrams = base_text.ngrams()
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
        """Gives skipgrams.

        Returns list of skipgrams, similar to ngram, but allows spacing between
        tokens.

        Args::
            gram_size : :obj:`int`, optional
            skip_size : :obj:`int`, optional

        Returns:
            :obj:`list`
                List of skipgrams, each ngram is a tuple the length of the gram_size

        Example:
            >>> base_text = BaseText('They hated to think of sample sentences.')
            >>> basic_skipgrams = base_text.skipgrams()
            >>> print(basic_skipgrams)
            [('They', 'hated', 'to'), ('They', 'hated', 'think'), ('They', 'to', 'think'), ('hated', 'to', 'think'), ('hated', 'to', 'of'), ('hated', 'think', 'of'), ('to', 'think', 'of'), ('to', 'think', 'sample'), ('to', 'of', 'sample'), ('think', 'of', 'sample'), ('think', 'of', 'sentences'), ('think', 'sample', 'sentences'), ('of', 'sample', 'sentences'), ('of', 'sample', '.'), ('of', 'sentences', '.'), ('sample', 'sentences', '.')] # noqa
        """
        tokens = self.tokenize()
        return list(skipgrams(tokens, gram_size, skip_size))
