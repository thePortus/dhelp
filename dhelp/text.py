#!/usr/bin/python

import os
import importlib
import pip
import re
from collections import UserString

import nltk
from nltk.text import Text
from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from nltk.util import ngrams, bigrams, trigrams, skipgrams
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag

from . import settings


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
        >>> text = BaseText('Lorem ipsum dolor sit amet...')
        >>> print(text)
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
            >>> text = BaseText('Lorem ipsum dolor sit amet...')
            >>> stringified_text = text.stringify()
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
            >>> text = BaseText('Lorem\\nipsum do-\\nlor sit amet....\\n')
            >>> modified_text = text.rm_lines()
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

        Gives a new version of the text with only latin characters remaining,
        or Greek characters for Greek, texts, and so on. Defaults to assuming
        Latin based.

        Returns:
            :obj:`self.__class__` Returns new version of text, with non-letters removed

        Example:
            >>> text = BaseText('1αLorem ipsum 2βdolor sit 3γamet...')
            >>> modified_text = text.rm_nonchars()
            >>> print(modified_text)
            'Lorem ipsum dolor sit amet...'
        """ # noqa
        if self.options['language'] == 'greek':
            valid_chars_pattern = '([ʹ-Ϋά-ϡἀ-ᾯᾰ-῾ ])'
        else:
            valid_chars_pattern = '([A-Za-z ])'
        return self.__class__(
            "".join(re.findall(valid_chars_pattern, self.data)),
            self.options
        )

    def rm_edits(self):
        """Removes text inside editor's marks.

        Gives a new version with any text between editorial marks such as
        brackets or parentheses removed.

        Returns:
            :obj:`self.__class__` Returns new version of text, with editoria removed

        Example:
            >>> text = BaseText('Lore[m i]psum {dolo}r sit a(met)...')
            >>> modified_text = text.rm_edits()
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
            >>> text = BaseText('Lorem   ipsum dolor  sit        amet...')
            >>> modified_text = text.rm_spaces()
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
            >>> text = BaseText('Lorem ipsum dolor sit amet...')
            >>> print(text.re_search('Lorem ipsum'))
            True
            >>> print(text.re_search('Arma virumque cano'))
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
            >>> EnglishText('').setup()
        """
        # get root directory of nltk data
        nltk_root_dir = os.path.join(
            os.path.expanduser('~'),
            'nltk_data',
        )
        for nltk_package, nltk_package_dir in settings.NLTK_PACKAGES[
            self.options['language']
        ]:
            # check for package locally, if not extant, download
            if os.path.exists(os.path.join(nltk_root_dir, nltk_package_dir)):
                nltk.download(nltk_package)
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
        # check if cltk is already installed, if not, install it
        if not importlib.find_loader('cltk'):
            pip.main(['install', 'cltk'])
        # include cltk inline
        from cltk.corpus.utils.importer import CorpusImporter
        setup_language = self.options['language']
        # for ancient greek, change to 'greek' for purposes of cltk setup
        if setup_language == 'ancient greek':
            setup_language = 'greek'
        corpus_importer = CorpusImporter(setup_language)
        # loop through, check if extant, attempt to download, skip any errors
        for cltk_corpus in corpus_importer.list_corpora:
            print('Downloading', cltk_corpus)
            try:
                corpus_importer.import_corpus(cltk_corpus)
            except:
                print('Problem downloading', cltk_corpus, '(skipping)')
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
            >>> LatinText('Gallia est omnis divisa in partes tres').tokenize()
            ['Gallia', 'est', 'omnis', 'divisa', 'in', 'partes', 'tres']

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


class LatinText(CLTKMixin, BaseText):
    """Main class to interact with Latin-language texts.

    Provides Latin-specific CLTK functions for text passed upon construction.
    Most methods return a new version of the text, except those that give
    non-text results (e.g. pos tagging)

    Example:
        >>> from dhelp import LatinText
        >>> text = LatinText('Gallia est omnis divisa in partes tres')
        >>> print(text.lemmatize())
        gallia edo1 omne divido in pars tres
    """

    def __init__(self, text, options={}):
        options['language'] = 'latin'
        super().__init__(text=text, options=options)

    def macronize(self, mode='tag_ngram_123_backoff'):
        """Adds macrons (long vowel marks).

        Macrons distinguish long vowels from short. Distinguishing them is
        critical for the study of Latin poetry and occasionally is important
        in prose. Note that once you add macrons, long vowels are, for all
        intents and purposes, different letters than their short equivalents.

        Args:
            mode (:obj:`str`, optional) POS tagging method to use, 'tag_ngram_123_backoff', 'tag_tnt', or 'tag_crf'

        Returns:
            :obj:`self.__class__` New text with macrons added to long vowels

        Example:
            >>> text = LatinText('Arma virumque cano, Troiae qui primus ab oris')
            >>> print(text.macronize())
            arma virumque cano , trojae quī prīmus ab ōrīs
        """ # noqa
        from cltk.prosody.latin.macronizer import Macronizer
        mode = mode.lower()
        if (
            mode != 'tag_ngram_123_backoff' and
            mode != 'tag_tnt' and
            mode != 'tag_crf'
        ):
            return False
        return self.__class__(
            Macronizer(tagger=mode).macronize_text(self.data),
            self.options
        )

    def normalize(self):
        """Replaces 'j's with 'i's and 'v's with 'u's.

        Ancient texts did not use j's or 'v's (viz. Indiana Jones and the Last
        Crusade), but their usage in modern texts can throw off word counts,
        pattern mataching, and general text-analysis methods. This method
        converts these letters to their ancient versions.

        Returns:
            :obj:`self.__class__` New text with macrons added to long vowels

        Example:
            >>> text = LatinText('Arma virumque cano, Troiae qui primus ab oris')
            >>> print(text.normalize())
            Arma uirumque cano, Troiae qui primus ab oris
        """ # noqa
        from cltk.stem.latin.j_v import JVReplacer
        return self.__class__(
            JVReplacer().replace(self.data),
            self.options
        )

    def stemmify(self):
        """Returns text with only stems.

        An alternate method to lemmatization. Instead of converting to lemmata
        (principi -> princeps) converts to stemma (principi -> princp)

        Returns:
            :obj:`self.__class__` New text with stemma

        Example:
            >>> text = LatinText('Arma virumque cano, Troiae qui primus ab oris')
            >>> print(text.stemmify())
            arm vir cano, troi qui prim ab or
        """ # noqa
        from cltk.stem.latin.stem import Stemmer
        return self.__class__(
            Stemmer().stem(self.data.lower()),
            self.options
        )

    def clausulae(self):
        """Counts different kinds of prose clausulae.

        Examines prose for evidence for poetic rythms (clausulae). Returns a
        keyword/value dict with total counts for each kind of clausula.

        Returns:
            :obj:`list` of `str` Individual clausulae results

        Example:
            >>> text = LatinText('Arma virumque cano, Troiae qui primus ab oris')
            >>> print(text.clausulae())
            {'cretic + trochee': 0, '4th paeon + trochee': 0, '1st paeon + trochee': 0, 'substituted cretic + trochee': 0, '1st paeon + anapest': 0, 'double cretic': 0, '4th paeon + cretic': 0, 'molossus + cretic': 0, 'double trochee': 0, 'molossus + double trochee': 0, 'cretic + double trochee': 0, 'dactyl + double trochee': 0, 'choriamb + double trochee': 0, 'cretic + iamb': 0, 'molossus + iamb': 0, 'double spondee': 0, 'cretic + double spondee': 0, 'heroic': 0}
        """ # noqa
        from cltk.prosody.latin.clausulae_analysis import Clausulae
        return Clausulae().clausulae_analysis(self.data)


class AncientGreekText(CLTKMixin, BaseText):
    """Main class to interact with Classical Greek-language texts.

    Provides Classical Greek-specific CLTK functions for text passed upon
    construction. Most methods return a new version of the text, except those
    that give non-text results (e.g. pos tagging)

    Example:
        >>> from dhelp import AncientGreekText
        >>> text = AncientGreekText('ἔστι δὲ σύμπαντα ταῦτα τὰ συγγράμματα ἐκείνῃ μάλιστα οὐκ ὠφέλιμα, ὅτι ὡς πρὸς εἰδότας συγγέγραπται.')
        >>> print(text.lemmatize())
        εἰμί δὲ σύμπας οὗτος τὰ σύγγραμμα ἐκεῖνος μάλιστα οὐ ὠφέλιμος , ὅστις ὡς πρὸς οἶδα συγγράφω.
    """ # noqa

    def __init__(self, text, options={}):
        options['language'] = 'greek'
        super().__init__(text=text, options=options)

    def normalize(self):
        """Fixes problems with differences in greek accent encoding.

        Certain Greek accents have more than one possible encoding. Uses cltk's
        built-in normalizer to correct the character encoding differences and
        ensure that accents are encoded the same way.

        Returns:
            :obj:`self.__class__` New instance with altered text

        Example:
            >>> text = AncientGreekText('ῖν», εἰς δὲ τὸν ἕτερον κ[α]ττίτ[ερον «εἰ λῶιον καὶ ἄμει]νόν ἐστι')
            >>> print(text.normalize())
            ῖν», εἰς δὲ τὸν ἕτερον κ[α]ττίτ[ερον «εἰ λῶιον καὶ ἄμει]νόν ἐστι
        """ # noqa
        from cltk.corpus.utils.formatter import cltk_normalize
        return self.__class__(
            text=cltk_normalize(str(self.data)),
            options=self.options
        )

    def tlgu_cleanup(self, rm_punctuation=True, rm_periods=False):
        """Fix TLG betacode texts using TLGU.

        Necessary to cleanup TLG texts before processing, but can also used to
        perform rudimentary cleaning operations on other Greek texts.

        Args:
            rm_punctuation (:obj:`bool`, optional) True to remove punctuation marks (exception periods)
            rm_periods (:obj:`bool`, optional) True to remove periods

        Returns:
            :obj:`self.__class__` New instance with altered text

        Example:
            >>> text = AncientGreekText('ῖν», εἰς δὲ τὸν ἕτερον κ[α]ττίτ[ερον «εἰ λῶιον καὶ ἄμει]νόν ἐστι')
            >>> print(text.tlgu_cleanup())
            ῖν εἰς δὲ τὸν ἕτερον καττίτερον εἰ λῶιον καὶ ἄμεινόν ἐστι
        """ # noqa
        from cltk.corpus.utils.formatter import tlg_plaintext_cleanup
        return self.__class__(
            text=tlg_plaintext_cleanup(
                self.data, rm_punctuation=rm_punctuation, rm_periods=rm_periods
            ),
            options=self.options
        )

    def tag(self, mode='123'):
        """Gives words marked up with parts-of-speech.

        Override's the cltk POS tagger and uses cltk's instead. Has different
        methods for providing a POS tagger, if desired.

        Args:
            mode (:obj:`str`) Tagging mode, either '123', or 'tnt'

        Returns:
            :obj:`list` of :obj:`tuple` 2-tuples with word, part-of-speech

        Example:
            >>> text = AncientGreekText('ἔστι δὲ σύμπαντα ταῦτα τὰ συγγράμματα ἐκείνῃ μάλιστα οὐκ ὠφέλιμα, ὅτι ὡς πρὸς εἰδότας συγγέγραπται.')
            >>> print(text.tag())
            [('ἔστι', 'V3SPIA---'), ('δὲ', 'G--------'), ('σύμπαντα', None), ('ταῦτα', 'A-P---NA-'), ('τὰ', 'L-P---NA-'), ('συγγράμματα', None), ('ἐκείνῃ', 'A-S---FD-'), ('μάλιστα', 'D--------'), ('οὐκ', 'D--------'), ('ὠφέλιμα', None), (',', 'U--------'), ('ὅτι', 'C--------'), ('ὡς', 'C--------'), ('πρὸς', 'R--------'), ('εἰδότας', 'T-PRPAMA-'), ('συγγέγραπται', None), ('.', '---------')]
        """ # noqa
        from cltk.tag.pos import POSTag
        tagger = POSTag(self.options['language'])
        mode = mode.lower()
        if mode != '123' and mode != 'tnt':
            raise Exception(
                'Invalid part of speech tagging mode specified.'
            )
        elif mode == '123':
            return tagger.tag_ngram_123_backoff(self.data)
        elif mode == 'tnt':
            return tagger.tag_tnt(self.data)
