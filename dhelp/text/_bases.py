#!/usr/bin/python

import re
from collections import UserString


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
    options = {}

    def __init__(self, text, *args, **kwargs):
        super().__init__(str)
        self.options = {
            'encoding': 'utf-8',
            'language': 'english'
        }
        # update .options if options keyword arg passed
        if 'options' in kwargs:
            if type(kwargs['options']) == dict:
                self.options.update(kwargs['options'])
        self.data = text

    def __enter__(self):
        pass

    def __exit__(self, ctx_type, ctx_value, ctx_traceback):
        pass

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
