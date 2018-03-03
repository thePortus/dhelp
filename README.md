# dhelp

---

[![Build Status](https://travis-ci.org/thePortus/dhelp.svg?branch=master)](https://travis-ci.org/thePortus/dhelp) [![Coverage Status](https://coveralls.io/repos/github/thePortus/dhelp/badge.svg?branch=master)](https://coveralls.io/github/thePortus/dhelp?branch=master)

---

[David J. Thomas](mailto:dave.a.base@gmail.com), [thePortus.com](http://thePortus.com)<br />
Instructor of Ancient History and Digital Humanities,<br />
Department of History,<br />
[University of South Florida](https://github.com/usf-portal)

---

Python module with help objects for various Digital Humanities related tasks.
Contains submodules to work with text files/folders, CSVs, webpages, and
perform natural language processing.

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

---

# Documentation and Examples

Full project documentation hosted on readthedocs.io coming soon.

**Table of Contents**

* [Web Module](#web-module)
* [Files Module](#files-module)
* [Text Module](#text-module)

---

## Web Module

Module for scraping and processing web data. Primarily used for scraping web
pages.

Contains:

* [WebPage()](#WebPage())

---

### **WebPage()**

Provides methods to download/parse a specified webpage. Merges the request
package with [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
functions to enable users to request/soup
a page in a single line.

```python
from dhelp import WebPage

web_page = WebPage('https://stackoverflow.com')

# if printed to screen, WebPage will display the url to which it is connected
>>> print(web_page)
https://stackoverflow.com

```

---

#### WebPage.soup()

Invokes web request then returns a soup object loaded with page HTML

```python

# fetch webpage and parse into BeautifulSoup object
>>> parsed_webpage = WebPage('https://stackoverflow.com/').soup()

# grab the logo from the header with BeautifulSoup
>>> header_logo_text = parsed_webpage.find('header')
    .find('div', class_='-main')
    .find('span', class_='-img')

# print the text contained in the span tag
>>> print(header_logo_text.get_text())
Stack Overflow
```

---

## Files Module

Module for loading/saving/modifying individual or groups of files. Primarily
used for loading of plain text files (individually or by folder) or CSVs.

---

### **TextFile()**

Load and save plain text data to/from files with TextFile. Loads data located
at given path as a string. Likewise if .save() will save string data at the
system path send to TextFile

```python
>>> from dhelp import TextFile

>>> text_file = TextFile('some/path.txt')

# if printed to screen, TextFile will display the system path to which it is connected
>>> print(text_file)
some/path.txt
```

---

#### TextFile.load()

Opens file and returns contents as a single string.

```python

>>> from dhelp import TextFile

# load data from path and print
>>> file_data = TextFile('some/path.txt').load()
>>> print(file_data)
Lorem ipsum dolor sit amet...

```

---

#### TextFile.save()

Saves string data to file, won't overwrite unless option is flagged.

```python

>>> from dhelp import TextFile

# save string data to path then print path
>>> saved_text_file = TextFile('some/path.txt').save('Lorem ipsum dolor sit amet...')
>>> print(saved_text_file)
/absolute/path/to/some/path.txt

# overwrite previous data by passing options dictionary with 'overwrite' set
>>> options = {'overwrite': True}
>>> saved_text_file = saved_text_file.save('consectetur adipiscing elit', options=options)
>>> print(saved_text_file)
/absolute/path/to/some/path.txt


```

---

### **TextFolder()**

Can load or save a folder of plaintext files as a list of strings. Also enables
batch editing of an entire directory by passing a callback.

```python
>>> from dhelp import TextFolder

>>> text_folder = TextFolder('some/path')

# like TextFile, if printed to screen, TextFolder will display the system path to which it is connected
>>> print(text_folder)
some/path
```

---

#### TextFolder.text_files()

Load all .txt (or other types) in a folder as list of TextFile objects.

```python

# load .txts in folder as list of TextFile objs, each linked to file loc
>>> folder_files = TextFolder('some/path').text_files()
# loop through each TextFile object, load data and print
>>> for folder_file in folder_files:
>>>     print(folder_file.load())
Lorem ipsum dolor sit amet...

```

---

#### TextFolder.modify()

Opens every file and performs a callback function sent to it. Provides a fast
means of batch editing an entire folder of txt files. Returns a new TextFolder
linked with the modified copy.

```python

# make a function with a single arg which defines how to modify a single record
>>> def modify_record(record_data):
>>>     record_data = record_data.replace('\n', '')
>>>     return record_data

# if you don't specify destination, a backup will automatically be created
>>> options = {'destination': 'some/other-path'}

# use TextFolder().modify, pass your function as 1st arg
>>> text_folder = TextFolder('some/path').modify(modify_record, options=options)
>>> print(text_folder)
/absolute/path/to/some/path

```

---

### **CSVFile()**

Makes loading and saving CSV data a simple matter. Simplifies the use of the
csv.DictReader and csv.DictWriter for loading or saving csv's as lists of
dictionaries.

```python

>>> from dhelp import CSVFile

>>> csv_file = CSVFile('some/path.csv')

# if printed to screen, CSVFile will display the system path to which it is connected
>>> print(csv_file)
/absolute/path/to/some/path.csv

```

---

#### CSVFile().fieldnames

Opens CSV file and reads the first row to get column names.

```python

>>> csv_file = CSVFile('some/path.csv')
>>> print(csv_file.fieldnames)
['id', 'text', 'notes']

```

---

#### CSVFile().load()

Load csv data as list of dictionaries.

```python

>>> csv_file = CSVFile('some/path.csv')
>>> csv_data = CSVFile.load()
>>> print(csv_data)
[{'id': '1', 'text': 'Lorem ipsum', 'notes': ''}, {'id': '2', 'text': 'dolor sit', 'notes': ''}, {'id': '3', 'text': 'amet.', 'notes': ''}]

```

---

#### CSVFile().save()

Save a list of dictionaries to a .csv file. You must specify
the column headers (fieldnames) with a list of strings. Returns True
upon success.

```python
>>> fake_fieldnames = ['id', 'text', 'notes']
>>> fake_data = [{
        'id': '1',
        'text': 'Lorem ipsum',
        'notes': ''
    }, {
        'id': '2',
        'text': 'dolor sit',
        'notes': ''
    }, {
        'id': '3',
        'text': 'amet.',
        'notes': ''
    }]
>>> csv_file = CSVFile('some/path.csv').save(fake_data, fieldnames=fake_fieldnames)
>>> print(csv_file)
/absolute/path/to/some/path.csv

```

---

#### CSVFile().modify()

Copies CSV to destination then performs the modify_cb callback
function passed on each data row before saving the file. Quick way
to perform batch changes to a CSV. Returns new CSVFile object linked
to modified CSV.

```python

# define a function which describes how to modify any given data row
>>> def modify_function(csv_record):
>>>     csv_record['text'] = 'Lorem ipsum dolor sit amet...'
>>>     csv_record['notes'] = 'Edited with dhelp'
>>>     return csv_record

# pass a destination and your function as arguments to .modify()
>>> csv_file = CSVFile('some/path.csv')
>>> altered_csv_file = csv_file.modify('some/other-path.csv', modify_cb=modify_function)

# .modify will return a new CSVFile object tied to the new location
>>> print(altered_csv_file)
/absolute/path/to/some/other-path.csv

```

---

## Text Module

Module for text processing and natural language processing, primarily using
the natural language toolkit (nltk).

---

### **BasicText()**

Base class for all Text objects. Can be used on its own to perform a number
of operations, although it is best used with on of its language-specific
children.

```python

>>> from dhelp import BasicText

>>> basic_text = BasicText('Lorem ipsum dolor sit amet...')
>>> print(basic_text)
Lorem ipsum dolor sit amet...

```

---

#### BasicText().stringify()

Returns the text of this object as a pure string type.

```python

>>> basic_text = BasicText('Lorem ipsum dolor sit amet...')
>>> stringified_text = basic_text.stringify()
>>> print(type(stringified_text))
<class 'str'>


```

---

#### BasicText().rm_lines()

Gives a new version of the text with all endlines removed. Removes
any dashed line endings and rejoins split words.

```python

>>> basic_text = BasicText('Lorem\nipsum do-\nlor sit amet....\n')
>>> modified_text = basic_text.rm_lines()
>>> print(modified_text)
Lorem ipsum dolor sit amet...

```

---

#### BasicText().rm_nonchars()

Gives a new version of the text with only latin characters remaining.
Is overriden by child objects for languages using non latinate chars.

```python

>>> basic_text = BasicText('1αLorem ipsum 2βdolor sit 3γamet...')
>>> modified_text = basic_text.rm_nonchars()
>>> print(modified_text)
Lorem ipsum dolor sit amet...

```

---

#### BasicText().rm_edits()

Gives a new version with any text between editorial marks such as
brackets or parentheses removed. NOTE: May not work exactly as shown below,
the way this method deals with spaces inside or outside editorial marks needs
improvement.

```python

>>> basic_text = BasicText('Lore[m i]psum {dolo}r sit a(met)...')
>>> modified_text = basic_text.rm_edits()
>>> print(modified_text)
Lor psum r sit a...

```

---

#### BasicText().rm_spaces()

Gives a new version of the text with extra whitespace collapsed.

```python

>>> basic_text = BasicText('Lorem   ipsum dolor  sit               amet...')
>>> modified_text = basic_text.rm_spaces()
>>> print(modified_text)
Lorem ipsum dolor sit amet...

```

---

#### BasicText().rm_stopwords()

Given a list of words or phrases, gives new text with those phrases
removed.

```python

>>> stopwords = ['ipsum', 'sit']
>>> basic_text = BasicText('Lorem ipsum dolor sit amet...')
>>> modified_text = basic_text.rm_stopwords(stoplist=stopwords)
>>> print(modified_text)
Lorem dolor amet...

```

---

#### BasicText().lemmatize()

Gives a new version of the text in which every word is lemmatized. All verbs
are transformed into the first person singular present active, all nouns are
transformed into the singular masculine nominative, et.c. NOTE: May not work
exactly as below as this will be tweaked.

```python

>>> basic_text = BasicText('They hated to think of sample sentences.')
>>> modified_text = basic_text.lemmatize()
>>> print(modified_text)
I hate think of sample sentence.

```

---

#### BasicText().re_search()

Receives a [Regular Expression](https://regexr.com/) search pattern and returns
True/False if it matches.

```python

>>> basic_text = BasicText('Lorem ipsum dolor sit amet...')
>>> print(basic_text.re_search('Lorem ipsum'))
True
>>> print(basic_text.re_search('Arma virumque cano'))
False

```

---

#### BasicText().tokenize()

Returns a tokenized list. By default returns list of words, but can also return
as a list of sentences.

```python

>>> basic_text = BasicText('Lorem ipsum dolor sit amet. Consectetur adipiscing elit.')
>>> print(BasicText.tokenize())
['Lorem', 'ipsum', 'dolor', 'sit', 'amet', '.', 'Consectetur', 'adipiscing', 'elit', '.']
>>> print(BasicText.tokenize(mode='sentence'))
['Lorem ipsum dolor sit amet.', 'Consectetur adipiscing elit.']

```

---

#### BasicText().tag()

Returns list of words marked up with parts of speech. Each word is returned as
a 2-tuple, the first containing the word, the second with the parts of speech.

```python

>>> basic_text = BasicText('They hated to think of sample sentences.')
>>> basic_tags = basic_text.tag()
>>> print(basic_tags)
[('They', 'PRP'), ('hated', 'VBD'), ('to', 'TO'), ('think', 'VB'), ('of', 'IN'), ('sample', 'JJ'), ('sentences', 'NNS'), ('.', '.')]

```

---

#### BasicText().ngrams()

Returns a list of ngrams, each ngram represented as a tuple.

```python

>>> basic_text = BasicText('They hated to think of sample sentences.')
>>> basic_ngrams = basic_text.ngrams()
>>> print(basic_ngrams)
[('They', 'hated', 'to'), ('hated', 'to', 'think'), ('to', 'think', 'of'), ('think', 'of', 'sample'), ('of', 'sample', 'sentences'), ('sample', 'sentences', '.')]

```

---

#### BasicText().skipgrams()

Returns list of skipgrams, similar to ngram, but allows spacing between tokens.

```python

>>> basic_text = BasicText('They hated to think of sample sentences.')
>>> basic_skipgrams = basic_text.skipgrams()
>>> print(basic_skipgrams)
[('They', 'hated', 'to'), ('They', 'hated', 'think'), ('They', 'to', 'think'), ('hated', 'to', 'think'), ('hated', 'to', 'of'), ('hated', 'think', 'of'), ('to', 'think', 'of'), ('to', 'think', 'sample'), ('to', 'of', 'sample'), ('think', 'of', 'sample'), ('think', 'of', 'sentences'), ('think', 'sample', 'sentences'), ('of', 'sample', 'sentences'), ('of', 'sample', '.'), ('of', 'sentences', '.'), ('sample', 'sentences', '.')]

```
