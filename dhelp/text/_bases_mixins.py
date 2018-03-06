#!/usr/bin/python

import re
from collections import UserString

import nltk
from nltk.text import Text
from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from nltk.util import ngrams, bigrams, trigrams, skipgrams
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag


class BaseText(UserString):
    """Performs text manipulation and natural language processing.

    Base class for all Text objects. Can be used on its own to perform a number
    of operations, although it is best used with on of its language-specific
    children.

    Args:
        text (:obj:`str`) Text to be stored for processing/nlp
        options (:obj:`dict`, optional) Options settings found at respective keywords

    Example:
        >>> from dhelp import BaseText
        >>> base_text = BaseText('Lorem ipsum dolor sit amet...')
        >>> print(base_text)
        'Lorem ipsum dolor sit amet...'
    """ # noqa

    def __init__(self, text, options={}):
        super().__init__(str)
        if 'encoding' not in options:
            options['encoding'] = 'utf-8'
        if 'language' not in options:
            options['language'] = 'english'
        self.data = text
        self.options = options

    def stringify(self):
        """Returns the text of this object as a pure string type.

        Can be useful when you need the text back in a string object format
        for comparison with regular strings.

        Returns:
            :obj:`str` String form of the text

        Example:
            >>> base_text = BaseText('Lorem ipsum dolor sit amet...')
            >>> stringified_text = base_text.stringify()
            >>> print(type(stringified_text))
            <class 'str'>
        """
        return str(self.data)

    def rm_lines(self):
        """Removes endlines.

        Gives a new version of the text with all endlines removed. Removes
        any dashed line endings and rejoins split words.

        Returns:
            :obj:`self.__class__` New version of text, with endlines removed

        Example:
            >>> base_text = BaseText('Lorem\\nipsum do-\\nlor sit amet....\\n')
            >>> modified_text = base_text.rm_lines()
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
        """Removes non-language characters.

        Gives a new version of the text with only latin characters remaining.
        Is overriden by child objects for languages using non latinate chars.

        Returns:
            :obj:`self.__class__` Returns new version of text, with non-letters removed

        Example:
            >>> base_text = BaseText('1αLorem ipsum 2βdolor sit 3γamet...')
            >>> modified_text = base_text.rm_nonchars()
            >>> print(modified_text)
            'Lorem ipsum dolor sit amet...'
        """ # noqa
        return self.__class__(
            "".join(re.findall("([A-Za-z ])", self.data)),
            self.options
        )

    def rm_edits(self):
        """Removes text inside editor's marks.

        Gives a new version with any text between editorial marks such as
        brackets or parentheses removed.

        Returns:
            :obj:`self.__class__` Returns new version of text, with editoria removed

        Example:
            >>> base_text = BaseText('Lore[m i]psum {dolo}r sit a(met)...')
            >>> modified_text = base_text.rm_edits()
            >>> print(modified_text)
            'Lor psum r sit a...'
        """ # noqa
        return self.__class__(
            re.sub("\〚(.*?)\〛", "", re.sub("\{(.*?)\}", "", re.sub(
                "\((.*?)\)", "", re.sub("\<(.*?)\>", "", re.sub(
                    "\[(.*?)\]", "", self.data))))),
            self.options
        )

    def rm_spaces(self):
        """Removes extra whitespace.

        Gives a new version of the text with extra whitespace collapsed.

        Returns:
            :obj:`self.__class__` Returns new version of text, with extra spaced collapsed

        Example:
            >>> base_text = BaseText('Lorem   ipsum dolor  sit        amet...')
            >>> modified_text = base_text.rm_spaces()
            >>> print(modified_text)
            'Lorem ipsum dolor sit amet...'
        """ # noqa
        # regex compiler for all whitespace blocks
        rexr = re.compile(r'\s+')
        # substituting single spaces for matching whitespace blocks
        clean_text = rexr.sub(' ', self.data)
        return self.__class__(
            clean_text.strip(),
            self.options
        )

    def re_search(self, pattern):
        """Search text for matching pattern.

        Receives search pattern and returns True/False if it matches. Pattern
        can be a simple string match (e.g. .re_search('does this match?')), or
        a full Regular Expression.

        Args:
            pattern (:obj:`str`) String with the desired Regular Expression to search

        Returns:
            :obj:`bool` True if matching, False if not

        Example:
            >>> base_text = BaseText('Lorem ipsum dolor sit amet...')
            >>> print(base_text.re_search('Lorem ipsum'))
            True
            >>> print(base_text.re_search('Arma virumque cano'))
            False
        """ # noqa
        # Converting pattern to regex
        pattern = re.compile(pattern)
        if pattern.search(self.data):
            return True
        else:
            return False


class NLTKMixin:
    """Mixin for NLTK-related functions.

    Mixin class which provides access to NLTK-specific functions. This class
    should be mixed with some base class (e.g. EnglishText) to give it nlp
    related functions.

    Example:
        >>> class EnglishText(NLTKTextMixin, EnglishText):
    """

    def setup(self):
        """Download NLTK packages and trainer corpora.

        Launches the NLTK package download interface. Overridden by the CLTK
        child classes to launch the automated CLTK downloader. Convenience
        method if user has not already downloaded NLTK packages and trainer
        sets.

        Example:
            >>> EnglishText('').setup() # noqa
        """
        nltk.download()
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
            >>> base_text = EnglishText('Lorem ipsum dolor sit amet...')
            >>> base_text.rm_stopwords(stoplist=stopwords)
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
            >>> base_text = EnglishText('The quick brown fox jumped over the lazy dog.') # noqa
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
            mode (:obj:`str`) Specifies tokenize mode, either 'word', 'sentence', or 'wordpunct'

        Returns:
            :obj:`list` List of (string) tokens

        Example:
            >>> base_text = EnglishText('Lorem ipsum dolor sit amet. Consectetur adipiscing elit.') # noqa
            >>> print(EnglishText.tokenize())
            ['Lorem', 'ipsum', 'dolor', 'sit', 'amet', '.', 'Consectetur', 'adipiscing', 'elit', '.'] # noqa
            >>> print(EnglishText.tokenize(mode='sentence'))
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
            (:obj:`list`) Words tagged as 2-tuples (word|part of speech)

        Example:
            >>> base_text = EnglishText('They hated to think of sample sentences.')
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
            gram_size (:obj:`int`, optional) Size of the ngrams to generate

        Returns:
            :obj:`list` of :obj:`tuple` Words of each ngram

        Example:
            >>> base_text = EnglishText('They hated to think of sample sentences.')
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

        Args:
            gram_size (:obj:`int`, optional) Size of the ngrams to generate
            skip_size (:obj:`int`, optional) Size of max spacing allowed

        Returns:
            :obj:`list` of :obj:`tuple` Words of each skipgram

        Example:
            >>> base_text = EnglishText('They hated to think of sample sentences.')
            >>> basic_skipgrams = base_text.skipgrams()
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


class CLTKMixin(NLTKMixin):
    """Mixin for CLTK-related functions.

    Parent class for Latin, Classical Greek, and other CLTK language-specific
    objects. Provides access to universal CLTK commands with child classes
    adding some methods and overriding others.
    """

    def setup(self):
        """Download CLTK packages and trainer corpora.

        Launches the CLTK package download interface. Overridden by the CLTK
        child classes to launch the automated CLTK downloader. Convenience
        method if user has not already downloaded CLTK packages and trainer
        sets.

        Example:
            >>> LatinText('').setup()
        """
        from cltk.corpus.utils.importer import CorpusImporter
        corpus_importer = CorpusImporter(self.options['language'])
        # loop through and attempt to download, skip any errors
        for cltk_corpus in corpus_importer.list_corpora:
            print('Downloading', cltk_corpus)
            try:
                corpus_importer.import_corpus(cltk_corpus)
            except:
                print('Problem downloading', cltk_corpus, '(skipping)')
        print('Finished downloading corpora')
        return True

    def tokenize(self, mode='word'):
        """Tokenizes the passage into lists of words or sentences.

        Breaks text words into individual tokens (strings) by default. If
        mode is set to sentence, returns lists of sentences.

        Args:
            mode (:obj:`str`) Mode of tokenization, either 'word' or 'sentence'

        Returns:
            :obj:`list` of :obj:`str` Tokenized words (or sentences)

        Example:
            >>> # TODO:

        """
        from cltk.tokenize.word import nltk_tokenize_words
        from cltk.tokenize.sentence import TokenizeSentence
        if mode == 'sentence':
            return TokenizeSentence(
                self.options['language']
            ).tokenize_sentences(self.data)
        else:
            return nltk_tokenize_words(self.data)

    def lemmatize(self, return_string=True, return_raw=False):
        """Transforms words into their lemmata.

        Gives a new version of the text in which every word is lemmatized. All
        verbs are transformed into the first person singular present active,
        all nouns are transformed into the singular masculine nominative, et.c.

        Returns:
            :obj:`self.__class__` New version of the text with tokens transformed to their lemmata

        Example:
            >>> text = LatinText('Gallia est omnis divisa in partes tres')
            >>> print(text.lemmatize())
            gallia edo1 omne divido in pars tres
        """ # noqa
        from cltk.stem.lemma import LemmaReplacer
        return self.__class__(
            text=LemmaReplacer(
                self.options['language']
            ).lemmatize(
                self.data.lower(),
                return_string=return_string,
                return_raw=return_raw
            ),
            options=self.options
        )

    # TODO: This function does not work for Greek currently
    def scansion(self):
        """Gives list of scanned feet.

        Returns list of strings, each string representing the beats of a given
        foot. As in standard notation, dactyls are marked as '¯' and spondee's
        as '˘'.

        Returns:
            :obj:`list` Scanned feet

        Example:
            >>> text = LatinText('Arma virumque cano, Troiae qui primus ab oris')
            >>> print(text.scansion())
            ['¯˘˘¯˘˘˘˘˘¯˘˘˘˘˘x']
        """ # noqa
        if self.options['language'] == 'greek':
            from cltk.prosody.greek.scanner import Scansion as GreekScansion
            return GreekScansion().scan_text(self.data)
        elif self.options['language'] == 'latin':
            from cltk.prosody.latin.scanner import Scansion as LatinScansion
            return LatinScansion().scan_text(self.data)

    def entities(self, lemmatize=False, unique=False):
        """Returns a list of entities recognized in the text.

        Uses cltk's built in named-entity recognition. Reorganizes cltk's raw
        output from list of tuples to list of strings. Every entity recognized
        is added to the list returned. Unless unique option is set, entities
        which appear multiple times will be returned multiple times in the
        list.

        Args:
            lemmatize (:obj:`bool`, optional) Set True to lemmatize text before searching for entities
            unique (:obj:`bool`, optional) Set True and no entity appears in the return list more than once
        Example:
            >>> text = LatinText('Gallia est omnis divisa in partes tres')
            >>> print(text.entities())
            ['Gallia']
        """ # noqa
        from cltk.stem.lemma import LemmaReplacer
        from cltk.tag import ner
        entity_list = []
        # filtering non-entities
        for result in ner.tag_ner(
            self.options['language'],
            input_text=self.data,
            output_type=list
        ):
            # appending if item flagged as entity in tuple[1]
            try:
                if result[1] == 'Entity':
                    entity_list.append(result[0])
            # do nothing if 'Entity' not specified
            except:
                pass
            # removing duplicate entities if unique option specified
        if unique:
            entity_list = list(set(entity_list))
        # lemmatizing entities if option has been specified
        if lemmatize:
            entity_list = LemmaReplacer(self.options['language']).lemmatize(
                entity_list,
                return_string=False,
                return_raw=False
            )
        return entity_list

    # currently not working, TODO: fix or remove this code
    # def compare_levenshtein(self, other_text):
    #     """Gives the levenshtein difference between this and any passed text.
    #
    #     Args:
    #         other_text (:obj:`str`) String for comparison
    #
    #     Returns:
    #         :obj:`float` Levenshtein difference between texts
    #
    #     Example:
    #         >>> # TODO:
    #
    #     """ # noqa
    #     from cltk.text_reuse.levenshtein import Levenshtein
    #     return Levenshtein().ratio(self.data, other_text)

    def compare_longest_common_substring(self, other_text):
        """Gives the longest excerpt that this and any passed text have in common.

        Args:
            other_text (:obj:`str`) String for comparison

        Returns:
            :obj:`str` Longest common substring

        Example:
            >>> text = LatinText('Gallia est omnis divisa in partes tres')
            >>> print(text.compare_longest_common_substring('Galliae sunt omnis divisae in partes tres'))
            in partes tres
        """ # noqa
        from cltk.text_reuse.comparison import long_substring
        return long_substring(self.data, other_text)

    def compare_minhash(self, other_text):
        """Gives the minimum hash between this and any passed text.

        Args:
            other_text (:obj:`str`) String for comparison

        Returns:
            :obj:`float` Minimum hash between texts

        Example:
            >>> text = LatinText('Gallia est omnis divisa in partes tres')
            >>> print(text.compare_minhash('Galliae sunt omnis divisae in partes tres'))
            0.6444444444444445
        """ # noqa
        from cltk.text_reuse.comparison import minhash
        return minhash(self.data, other_text)

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
            >>> text = LatinText('Gallia est omnis divisa in partes tres tres tres')
            >>> print(text.word_count(word='tres'))
            3
        """ # noqa
        from cltk.utils.frequency import Frequency
        counts = Frequency().counter_from_str(self.data)
        # If a single word was specified, only return that frequency
        if word:
            return counts[word]
        return counts
