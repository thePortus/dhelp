# dhelp

*DH Python tools for scraping web pages, pre-processing data, and performing nlp analysis quickly*

---

[![PyPI version](https://badge.fury.io/py/dhelp.svg)](https://badge.fury.io/py/dhelp)
 [![Build Status](https://travis-ci.org/thePortus/dhelp.svg?branch=master)](https://travis-ci.org/thePortus/dhelp) [![Coverage Status](https://coveralls.io/repos/github/thePortus/dhelp/badge.svg?branch=master)](https://coveralls.io/github/thePortus/dhelp?branch=master) [![Documentation Status](https://readthedocs.org/projects/dhelp/badge/?version=latest)](http://dhelp.readthedocs.io/en/latest/?badge=latest) [![Code Health](https://landscape.io/github/thePortus/dhelp/master/landscape.svg?style=flat)](https://landscape.io/github/thePortus/dhelp/master) [![Total GitHub downloads](https://img.shields.io/github/downloads/thePortus/dhelp/total.svg)](https://img.shields.io/github/downloads/thePortus/dhelp/total.svg) [![Waffle.io - Columns and their card count](https://badge.waffle.io/thePortus/dhelp.svg?columns=all)](https://waffle.io/thePortus/dhelp)


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

# Table of Contents

* [Installation](#installation)
* [Language Setup](#language-setup)
* [Web Module](#web-module)
    * [WebPage](#webpage)
* [File Module](#file-module)
    * [TextFile](#textfile)
    * [TextFolder](#textfolder)
    * [CSVFile](#csvfile)
* [Text Module](#text-module)
    * [EnglishText](#englishtext)
    * [LatinText](#latintext)
    * [AncientGreekText](#ancientgreektext)
* [Combining Methods](#using-objects-together)

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

# Language Setup

The first time you use a language-specific text object, you need to run its .setup() method

```sh
from dhelp import EnglishText

EnglishText.setup()

```

---

# Files Module

Use the file module to load a file as a string in a single line of code. Or,
alter every text file in a folder by passing a simple function. Convert a
column of text data in a .csv file into a series of .txt files, again in a
single line of code.

## TextFile

**Main Examples**

```python

from dhelp import TextFile

# quickest method to modify a file, start by making a TextFile object...
txt_file = TextFile('some/file.txt')
# then use with/as syntax to give you the file contents in strings form
with txt_file as txt_data:
    # txt_data is contents, whatever you put in txt_file.save_data is saved
    txt_file.save_data = txt_data.replace('\n', '')

# Other methods...

# load file data as a string and print to screen
text_file = TextFile('some/file.txt')
text_file.load()
'Lorem ipsum dolor sit amet...'

# save string data to a file, returns self if successful
text_file = TextFile('some/file.txt')
text_file.save('Lorem ipsum dolor sit amet...')
'some/file.txt'

```

**Other Functions**

```python

# use a dict to specify options, including overwriting existing files
options = {
    'encoding': 'utf-8' # set character encoding for loading/saving
    'silent': False # set True to supress messages during loading/saving
    'overwrite': False # set True to save over any previous file
}
text_file = TextFile('some/file.txt').save('Lorem ipsum dolor sit amet...', options=options)

# check if a file exists at a location
TextFile('some/file.txt').exists
True

# move, copy, or delete files
TextFile('some/file.txt').move(destination='some/other-file.txt')
TextFile('some/other-file.txt').copy(destination='some/file.txt')
TextFile('some/other-file.txt').remove()

```

## TextFolder

**Main Examples**

```python

from dhelp import TextFolder

# quickest way to modify a folder, start by making a TextFolder object
text_folder = TextFolder('some/path')
# use with/as syntax to get a list of TextFile objects, then loop through
with text_folder as txt_files:
    for txt_file in txt_files:
        # use with/as syntax on file to get contents
        with txt_file as txt_data:
            # whatever you store in .save_data will be saved to file
            txt_file.save_data = txt_data.replace('\n', '')

```

**Other Methods**

```python

# returns a list of TextFile objects, each connected to a file in the folder
folder_files = TextFolder('some/folder').text_files
# You can loop through and load, edit, save, et.c. the TextFiles as normal
for folder_file in folder_files:
    # load the file as a string
    file_data = folder_file.load()
    # replace all endline characters with nothing
    file_data = file_data.replace('\n', '')
    # save altered data back to the file, specifying overwrite option
    folder_file.save(file_data, {'overwrite': True})

# .modify - a quick method to load/edit/and save all at once

# first, make a function showing how you want to alter the data of each file
# it gets 1 arg, the file str data, and returns 1 arg, the altered str data
def modify_file(file_data):
    # replace all endline characters with nothing and then return
    return file_data.replace('\n', '')

# send an output location and modify_file function as args and you are done!
TextFolder('some/folder').modify('some/other-folder', modify_file)

```

**Other Functions**

```python

# use a dict to specify options, including overwriting existing files
options = {
    'encoding': 'utf-8' # set character encoding for loading/saving
    'silent': False # set True to supress messages during loading/saving
    'overwrite': False # set True to save over any previous file
}

TextFolder('some/folder').modify('some/other-folder', modify_file, options=options)

# check if a folder exists at a location
TextFile('some/folder').exists
True

# move, copy, or delete folders
TextFile('some/folder').move(destination='some/other-folder')
TextFile('some/other-folder').copy(destination='some/folder')
TextFile('some/other-folder').remove()

```

## CSVFile

**Main Examples**

```python

# load CSV data as a list of dictionaries
csv_file = CSVFile('some/file.csv')
csv_file.load()
[{'id': '1', 'text': 'Lorem ipsum', 'notes': ''}, {'id': '2', 'text': 'dolor sit', 'notes': ''}, {'id': '3', 'text': 'amet.', 'notes': ''}]

# read column fieldnames of an existing csv
csv_file = CSVFile('some/file.csv')
csv_file.fieldnames
['id', 'text', 'notes']

# save a list of dictionary records to a csvfile
fake_data = [
    {'id', '1', 'text': 'Lorem ipsum'},
    {'id', '2', 'text': 'dolor sit'},
    {'id', '3', 'text': 'amet'}
]
fake_data_fieldnames = ['id', 'text']
csv_file = CSVFile('some/file.csv')
csv_file.save(fake_data, fake_data_fieldnames)
'some/file.csv'

# . modify - like TextFolder, load/edit/save every record

# like TextFolder, define a function, this time editing each record's data
def modify_csv_row(row_data):
    # the data will come in the form of a dictionary
    # here we just transform all text entries to lower case
    row_data['text'] = row_data['text'].lower()
    return row_data

# now call .modify, sending an output location and the function as args
CSVFile('some/file.csv').modify('some/other-file.csv', modify_csv_row)

```

**Other Functions**

```python

# check if a csv exists at a location
CSVFile('some/file.csv').exists
True

# move, copy, or delete csvs
CSVFile('some/file.csv').move(destination='some/other-file.csv')
CSVFile('some/other-file.csv').copy(destination='some/file.csv')
CSVFile('some/other-file.csv').remove()

```

# Web Module

## WebPage

With the web module, you can download a webpage and parse it into a
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) object with
one command.

*Examples*

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

# Text Module

The text module attaches mutiple methods for text cleaning/analysis that can
be easily accessed. Use one of the Text classes to get a string-like object
that comes with many convenient cleaning/nlp methods attached. You can chain
any of the string transformation methods to perform many text operations at
once.

## EnglishText

**Setup: Download the English Corpora**

Before you use this object for any of the methods below you need to download trainer corpora.

```python
from dhelp import EnglishText
EnglishText.setup()
```

**Examples**

```python

# .rm_lines() - remove endline characters
text = EnglishText('The qui\\nck brown fox jumped over the lazy dog')
text.rm_lines()
'The quick brown fox jumped over the lazy dog'

# .rm_nonchars() - remove non-letters
text = EnglishText('Th3e quick brown fox jumped over the lazy dog')
text.rm_nonchars()
'The quick brown fox jumped over the lazy dog'

# .rm_edits() - remove text between editorial marks
text = EnglishText('The [quick] brown fox jumped over the lazy dog')
text.rm_edits()
'The brown fox jumped over the lazy dog'

# .rm_spaces() - collapses redundant whitespaces
text = EnglishText('Th3e qui\\nck b     rown fox jumped over the lazy dog')
text.rm_spaces()
'The quick brown fox jumped over the lazy dog'

# .re_search() - checks for a given pattern
text = EnglishText('The quick brown fox jumped over the lazy dog')
text.re_search('fox')
True
text.re_search('lemur')
False

# .rm_stopwords() - removes a list of words from text
text = EnglishText('The quick brown fox jumped over the lazy dog')
text.rm_stopwords(['quick', 'brown','lazy'])
'The fox jumped over the dog'

# chain methods to perform them in one command
text = EnglishText('Th3e qui\\nck b     rown fox jumped over the lazy dog')
text.rm_lines().rm_nonchars().rm_spaces()
'The quick brown fox jumped over the lazy dog'

# lemmatize a text to make word counts/analysis
text = EnglishText('The quick brown fox jumped over the lazy dog.')
text.lemmatize()
'The quick brown fox jump over the lazy dog .'

# get 'tokens' (list of words)
text = EnglishText('The quick brown fox jumped over the lazy dog.')
EnglishText.tokenize()
['The', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy', 'dog']

# get word tallys
text = EnglishText('The quick brown fox jumped over the lazy dog.')
EnglishText.word_count()
{'The': 1, 'quick': 1, 'brown': 1, 'fox': 1, 'jumped': 1, 'over': 1, 'the': 1, 'lazy': 1, 'dog': 1}

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

## LatinText

**Setup: Download the Latin Corpora**

Before you use this object for any of the methods below you need to download trainer corpora.

```python

from dhelp import LatinText
LatinText('').setup()

```

**Examples**

```python

# .rm_lines() - remove endline characters
text = LatinText('Gallia \\nest omnis divisa in partes tres')
text.rm_lines()
'Gallia est omnis divisa in partes tres'

# .rm_nonchars() - remove non-letters
text = LatinText('Ga3llia est omnis divisa in partes tres')
text.rm_nonchars()
'Gallia est omnis divisa in partes tres'

# .rm_edits() - remove text between editorial marks
text = LatinText('Gallia est [omnis] divisa in partes tres)
text.rm_edits()
'Gallia est omnis divisa in partes tres'

# .rm_spaces() - collapses redundant whitespaces
text = LatinText('Gallia    est omnis divisa       in partes        tres')
text.rm_spaces()
'Gallia est omnis divisa in partes tres'

# .re_search() - checks for a given pattern
text = LatinText('Gallia est omnis divisa in partes tres')
text.re_search('Gallia')
True
text.re_search('Graecia')
False

# .rm_stopwords() - removes a list of words from text
text = LatinText('Gallia est omnis divisa in partes tres')
text.rm_stopwords(['est', 'in'])
'Gallia omnis divisa partes tres'

# chain methods to perform them in one command
text = LatinText('Ga3llia    \\nest omnis divisa       in partes        tres')
text.rm_lines().rm_nonchars().rm_spaces()
'Gallia est omnis divisa in partes tres'

# tokenize words into list of strings
text = LatinText('Gallia est omnis divisa in partes tres')
text.tokenize()
['Gallia', 'est', 'omnis', 'divisa', 'in', 'partes', 'tres']

# lemmatize the text
text = LatinText('Gallia est omnis divisa in partes tres')
text.lemmatize()
'gallia edo1 omne divido in pars tres'

# generate ngrams...
text = LatinText('Gallia est omnis divisa in partes tres')
text.ngrams()
[('Gallia', 'est', 'omnis'), ('est', 'omnis', 'divisa'), ('omnis', 'divisa', 'in'), ('divisa', 'in', 'partes'), ('in', 'partes', 'tres')]

# ... or skipgrams
text = LatinText('Gallia est omnis divisa in partes tres')
text.skipgrams()
[('Gallia', 'est', 'omnis'), ('est', 'omnis', 'divisa'), ('omnis', 'divisa', 'in'), ('divisa', 'in', 'partes'), ('in', 'partes', 'tres')]

# count all words
text = LatinText('Gallia est omnis divisa in partes tres tres tres')
text.word_count(word='tres')
3

# scan text for meter
text = LatinText('Arma virumque cano, Troiae qui primus ab oris')
text.scansion()
['¯˘˘¯˘˘˘˘˘¯˘˘˘˘˘x']

# get recognized entities as a list
text = LatinText('Gallia est omnis divisa in partes tres')
text.entities()
['Gallia']

# macronize vowels
text = LatinText('Arma virumque cano, Troiae qui primus ab oris')
text.macronize()
'arma virumque cano , trojae quī prīmus ab ōrīs'

# search for known entities
text = LatinText('Gallia est omnis divisa in partes tres')
text.entities()
['Gallia']

# compare for longest common substring
text = LatinText('Gallia est omnis divisa in partes tres')
text.compare_longest_common_substring('Galliae sunt omnis divisae in partes tres')
'in partes tres'

# compare minhash's
text = LatinText('Gallia est omnis divisa in partes tres')
text.compare_minhash('Galliae sunt omnis divisae in partes tres')
0.6444444444444445

```

## AncientGreekText

**Setup: Download the Greek Corpora**

Before you use this object for any of the methods below you need to download trainer corpora.

```python

from dhelp import AncientGreekText
AncientGreekText('').setup()

```

**Examples**

```python

# .rm_lines() - remove endline characters
text = AncientGreekText('ἔνθα \nποτὲ Ἀθηναίοις ἦν ἀργύρου μέταλλα'')
text.rm_lines()
'ἔνθα ποτὲ Ἀθηναίοις ἦν ἀργύρου μέταλλα

# .rm_nonchars() - remove non-letters
text = AncientGreekText('ἔν3θα ποτὲ Ἀθηναίοις ἦν ἀργύρου μέταλλα'')
text.rm_nonchars()
'ἔνθα ποτὲ Ἀθηναίοις ἦν ἀργύρου μέταλλα'

# .rm_edits() - remove text between editorial marks
text = AncientGreekText('ἔνθα ποτὲ Ἀθηναίοις ἦν ἀργύρου μέταλλα')
text.rm_edits()
'ἔνθα ποτὲ Ἀθηναίοις ἦν ἀργύρου μέταλλα'

# .rm_spaces() - collapses redundant whitespaces
text = AncientGreekText('ἔνθα      ποτὲ     Ἀθηναίοις ἦν ἀργύρου μέταλλα)
text.rm_spaces()
'ἔνθα ποτὲ Ἀθηναίοις ἦν ἀργύρου μέταλλα'

# .re_search() - checks for a given pattern
text = AncientGreekText('ἔνθα ποτὲ Ἀθηναίοις ἦν ἀργύρου μέταλλα')
text.re_search('Ἀθηναίοις')
True
text.re_search('σπαρτίοις')
False

# .rm_stopwords() - removes a list of words from text
text = AncientGreekText('ἔνθα ποτὲ Ἀθηναίοις ἦν ἀργύρου μέταλλα')
text.rm_stopwords(['ποτὲ', 'ἀργύρου'])
'ἔνθα Ἀθηναίοις ἦν μέταλλα'

# chain methods to perform them in one command
text = AncientGreekText('ἔν3θα      \nποτὲ     Ἀθηναίοις ἦν ἀργύρου μέταλλα')
text.rm_lines().rm_nonchars().rm_spaces()
'ἔνθα ποτὲ Ἀθηναίοις ἦν ἀργύρου μέταλλα'

# normalize character encoding differences
text = AncientGreekText('ἔνθα ποτὲ Ἀθηναίοις ἦν ἀργύρου μέταλλα')
text.normalize()
'ἔνθα ποτὲ Ἀθηναίοις ἦν ἀργύρου μέταλλα'

# perform text cleanup, designed for tlg texts
text = AncientGreekText('ῖν», εἰς δὲ τὸν ἕτερον κ[α]ττίτ[ερον «εἰ λῶιον καὶ ἄμει]νόν ἐστι')
text.tlgu_cleanup()
'ῖν εἰς δὲ τὸν ἕτερον καττίτερον εἰ λῶιον καὶ ἄμεινόν ἐστι'

# tokenize words into list of strings
text = AncientGreekText('ἔνθα ποτὲ Ἀθηναίοις ἦν ἀργύρου μέταλλα')
text.tokenize()
['ἔνθα', 'ποτὲ', 'Ἀθηναίοις', 'ἦν', 'ἀργύρου', 'μέταλλα']

# lemmatize the text
text = AncientGreekText('ἔνθα ποτὲ Ἀθηναίοις ἦν ἀργύρου μέταλλα')
text.lemmatize()
'ἔνθα ποτὲ ἀθηναῖος εἰμί ἀργυρόω μέταλλον'

# generate ngrams...
text.ngrams()
[('ἔνθα', 'ποτὲ', 'Ἀθηναίοις'), ('ποτὲ', 'Ἀθηναίοις', 'ἦν'), ('Ἀθηναίοις', 'ἦν', 'ἀργύρου'), ('ἦν', 'ἀργύρου', 'μέταλλα')]

# ... or skipgrams
text = AncientGreekText('ἔνθα ποτὲ Ἀθηναίοις ἦν ἀργύρου μέταλλα')
text.skipgrams()
[('ἔνθα', 'ποτὲ', 'Ἀθηναίοις'), ('ἔνθα', 'ποτὲ', 'ἦν'), ('ἔνθα', 'Ἀθηναίοις', 'ἦν'), ('ποτὲ', 'Ἀθηναίοις', 'ἦν'), ('ποτὲ', 'Ἀθηναίοις', 'ἀργύρου'), ('ποτὲ', 'ἦν', 'ἀργύρου'), ('Ἀθηναίοις', 'ἦν', 'ἀργύρου'), ('Ἀθηναίοις', 'ἦν', 'μέταλλα'), ('Ἀθηναίοις', 'ἀργύρου', 'μέταλλα'), ('ἦν', 'ἀργύρου', 'μέταλλα')]

# perform part-of-speech tagging
text = AncientGreekText('ἔνθα ποτὲ Ἀθηναίοις ἦν ἀργύρου μέταλλα')
text.tag()
[('ἔνθα', 'D--------'), ('ποτὲ', 'G--------'), ('Ἀθηναίοις', None), ('ἦν', 'V3SIIA---'), ('ἀργύρου', 'N-S---MG-'), ('μέταλλα', None)]

# search for known entities
text = AncientGreekText('ἔνθα ποτὲ Ἀθηναίοις ἦν ἀργύρου μέταλλα')
text.entities()
['Ἀθηναίοις']

# compare for longest common substring
text = AncientGreekText('ἔνθα ποτὲ Ἀθηναίοις ἦν ἀργύρου μέταλλα')
text.compare_longest_common_substring('ἔνθα Ἀθηναίοις ἀργύρου μέταλλα')
'ἀργύρου μέταλλα'

# compare minhash's
AncientGreekText('ἔνθα ποτὲ Ἀθηναίοις ἦν ἀργύρου μέταλλα')
text.compare_minhash('Ἀθηναίοις ἦν μέταλλα')
0.4594594594594595

# count all words
text = AncientGreekText('ἔνθα ποτὲ Ἀθηναίοις ἦν ἀργύρου μέταλλα')
text.word_count(word='Ἀθηναίοις')
1


```

---

# Using Objects Together

Lemmatizing an entire folder of Latin text files

```python

from dhelp import TextFolder, LatinText

# define a function which defines how each file's data will be modified (in this case removing extra spaces and lemmatizing)
def modify_function(file_data):
    file_data = LatinText(file_Data)
    return file_data.rm_space().lemmatize()

# create a TextFolder object tied to the location of the Latin txt files
text_folder = TextFolder('path/to/latin/files')
# call the modify method, sending the output path and the name of the function you defined
text_folder.modify('path/to/latin/files-lemmatized', modify_function)

# That's it, you will now have a folder full of lemmatized Latin files

```

More Examples Coming Soon
