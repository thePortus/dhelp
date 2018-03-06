# dhelp

*DH Python tools for scraping web pages, pre-processing data, and performing nlp analysis quickly*

---

[![Build Status](https://travis-ci.org/thePortus/dhelp.svg?branch=master)](https://travis-ci.org/thePortus/dhelp) [![Coverage Status](https://coveralls.io/repos/github/thePortus/dhelp/badge.svg?branch=master)](https://coveralls.io/github/thePortus/dhelp?branch=master) [![Documentation Status](https://readthedocs.org/projects/dhelp/badge/?version=latest)](http://dhelp.readthedocs.io/en/latest/?badge=latest)

---

[David J. Thomas](mailto:dave.a.base@gmail.com), [thePortus.com](http://thePortus.com)<br />
Instructor of Ancient History and Digital Humanities,<br />
Department of History,<br />
[University of South Florida](https://github.com/usf-portal)

---

Check out the full project documentation [dhelp.readthedocs.io](http://dhelp.readthedocs.io)

Made for my students.

Students often see great potential for Python in Historical Analysis. But,
before they see real payoff they often face too many hurdles to overcome in
the space of a single semester. dhelp is a tool to allow students to quickly
get to performing quick file operations, data manipulations, and even text
analysis.

---

Requires [Python 3.x](https://python.org)

---

# Installation

Install with pip (recommended)

```sh

pip install dhelp

```

or...

Use easy_install

```sh

# clone the repo and move into the directory
git clone https://github.com/thePortus/dhelp.git && cd dhelp
# run easy_install
easy_install setup.py

```

## Greek & Latin Users

If you want to work with CLTK tools, you must either `pip install -r requirements/dev.txt` from the root of this repo, or just type `pip install cltk`. Then, before you use a Text object for the first time, run LatinText('').setup() (or GreekText)

---

# Quickstart Guide

## Files Module

Use the file module to load a file as a string in a single line of code. Or,
alter every text file in a folder by passing a simple function. Convert a
column of text data in a .csv file into a series of .txt files, again in a
single line of code.

```python

from dhelp import TextFolder, TextFile

# load file data as a string and print to screen
file_data = TextFile('some/file.txt').load()
print(file_data)
'Lorem ipsum dolor sit amet...'

# get list of TextFiles, one for each .txt in folder
folder_files = TextFolder('some/folder').text_files
# loop through each file, load, and print to screen
for folder_file in folder_files:
    print(folder_file.load())
'Lorem ipsum dolor sit amet'
'consectetur adipiscing elit'
'sed do eiusmod tempor'
```

## Web Module

With the web module, you can download a webpage and parse it into a
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) object with
one command.

```python

from dhelp import WebPage

# make beautifulsoup object
page_soup = WebPage('https://stackoverflow.com').soup()
# narrow down to the element desired by chaining .find()
header_logo_text = page_soup.find('header')
    .find('div', class_='-main')
    .find('span', class_='-img')
 # print the text contained in the span tag
print(header_logo_text.get_text())
'Stack Overflow'
```

## Text Module

The text module attaches mutiple methods for text cleaning/analysis that can
be easily accessed. Use one of the Text classes to get a string-like object
that comes with many convenient cleaning/nlp methods attached. You can chain
any of the string transformation methods to perform many text operations at
once.

#### All Languages

**All Languages Have These Methods**

Examples...

```python

# .rm_lines() - remove endline characters
text = EnglishText('The qui\\nck brown fox jumped over the lazy dog')
text.rm_lines()
The quick brown fox jumped over the lazy dog

# .rm_nonchars() - remove non-letters
text = EnglishText('Th3e quick brown fox jumped over the lazy dog')
text.rm_nonchars()
The quick brown fox jumped over the lazy dog

# .rm_edits() - remove text between editorial marks
text = EnglishText('Th3e qui\\nck b     rown fox jumped over the lazy dog')
text.rm_edits()
The quick brown fox jumped over the lazy dog

# .rm_spaces() - collapses redundant whitespaces
text = EnglishText('Th3e qui\\nck b     rown fox jumped over the lazy dog')
text.rm_spaces()
The quick brown fox jumped over the lazy dog

# .re_search() - checks for a given pattern
text = EnglishText('The quick brown fox jumped over the lazy dog')
text.re_search('fox')
True
text.re_search('lemur')
False

# .rm_stopwords() - removes a list of words from text
text = EnglishText('The quick brown fox jumped over the lazy dog')
text.rm_stopwords(['quick', 'brown','lazy'])
The fox jumped over the dog

# chain methods to perform them in one command
text = EnglishText('Th3e qui\\nck b     rown fox jumped over the lazy dog')
text.rm_lines().rm_nonchars().rm_spaces()
The quick brown fox jumped over the lazy dog

```

#### English

**Setup: Download the English Corpora**

Before you use this object for any of the methods below you need to download trainer corpora.

```python
from dhelp import LatinText
EnglishText('').setup()
```

Examples...

```python

# lemmatize a text to make word counts/analysis
text = EnglishText('The quick brown fox jumped over the lazy dog.')
text.lemmatize()
'The quick brown fox jump over the lazy dog .'

# get 'tokens' (list of words)
text = EnglishText('The quick brown fox jumped over the lazy dog.')
EnglishText.tokenize()
['The', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy', 'dog']

# tag words with parts of speech
text = EnglishText('They hated to think of sample sentences.')
text.tag()
[('They', 'PRP'), ('hated', 'VBD'), ('to', 'TO'), ('think', 'VB'), ('of', 'IN'), ('sample', 'JJ'), ('sentences', 'NNS'), ('.', '.')]

# generate ngrams...
text = EnglishText('They hated to think of sample sentences.')
text.ngrams()
[('They', 'hated', 'to'), ('hated', 'to', 'think'), ('to', 'think', 'of'), ('think', 'of', 'sample'), ('of', 'sample', 'sentences'), ('sample', 'sentences', '.')]

# ... or skipgrams
text = EnglishText('They hated to think of sample sentences.')
text.skipgrams()
[('They', 'hated', 'to'), ('They', 'hated', 'think'), ('They', 'to', 'think'), ('hated', 'to', 'think'), ('hated', 'to', 'of'), ('hated', 'think', 'of'), ('to', 'think', 'of'), ('to', 'think', 'sample'), ('to', 'of', 'sample'), ('think', 'of', 'sample'), ('think', 'of', 'sentences'), ('think', 'sample', 'sentences'), ('of', 'sample', 'sentences'), ('of', 'sample', '.'), ('of', 'sentences', '.'), ('sample', 'sentences', '.')]

```

#### Greek & Latin

**Note: Greek & Latin Classes inherit all methods from EnglishText**

**Setup: Download the Latin Corpora**

Before you use this object for any of the methods below you need to download trainer corpora.

```python

from dhelp import LatinText
LatinText('').setup()

# OR

from dhelp import GreekText
GreekText('').setup()

```

```python

# macronize vowels
text = LatinText('Arma virumque cano, Troiae qui primus ab oris')
print(text.macronize())
arma virumque cano , trojae quī prīmus ab ōrīs

# search for known entities
text = LatinText('Gallia est omnis divisa in partes tres')
text.entities()
['Gallia']

# compare for longest common substring
text = LatinText('Gallia est omnis divisa in partes tres')
text.compare_longest_common_substring('Galliae sunt omnis divisae in partes tres')
in partes tres

# compare minhash's
LatinText('Gallia est omnis divisa in partes tres')
text.compare_minhash('Galliae sunt omnis divisae in partes tres')
0.6444444444444445

# count all words
text = LatinText('Gallia est omnis divisa in partes tres tres tres')
text.word_count(word='tres')

```

---

# Examples in Practice

Coming Soon
