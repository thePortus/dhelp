# dhelp

---

[![Build Status](https://travis-ci.org/thePortus/dhelp.svg?branch=master)](https://travis-ci.org/thePortus/dhelp) [![Coverage Status](https://coveralls.io/repos/github/thePortus/dhelp/badge.svg?branch=master)](https://coveralls.io/github/thePortus/dhelp?branch=master) [![Documentation Status](https://readthedocs.org/projects/dhelp/badge/?version=latest)](http://dhelp.readthedocs.io/en/latest/?badge=latest)

---

[David J. Thomas](mailto:dave.a.base@gmail.com), [thePortus.com](http://thePortus.com)<br />
Instructor of Ancient History and Digital Humanities,<br />
Department of History,<br />
[University of South Florida](https://github.com/usf-portal)

---

Python module with help objects for various Digital Humanities related tasks.
Contains submodules to work with text files/folders, CSVs, web pages, and
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
>>> from dhelp import WebPage
>>> web_page = WebPage('https://stackoverflow.com')
>>> print(web_page)
https://stackoverflow.com
>>> # pass an dict to set options for delay, max_retries, or silent
>>> options = {
...     'delay': 4,
        'max_retries': 3,
        'silent': True
... }
>>> web_page = WebPage('https://stackoverflow.com', options=options)

```

---

#### WebPage.fetch()

Returns http request from URL as a string.

```python

>>> html_text = WebPage('https://stackoverflow.com/').fetch()
Stack Overflow

```

---

#### WebPage.soup()

Invokes web request then returns a soup object loaded with page HTML

```python

>>> # fetch webpage and parse into BeautifulSoup object
>>> parsed_webpage = WebPage('https://stackoverflow.com/').soup()
>>> # grab the logo from the header with BeautifulSoup
>>> header_logo_text = parsed_webpage.find('header')
...    .find('div', class_='-main')
...    .find('span', class_='-img')
>>> # print the text contained in the span tag
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

>>> text_file = TextFile('some/path.txt')
>>> print(text_file)
some/path.txt

```

---

#### TextFile.load()

Opens file and returns contents as a single string.

```python

>>> file_data = TextFile('some/path.txt').load()
>>> print(file_data)
Lorem ipsum dolor sit amet...

```

---

#### TextFile.save()

Saves string data to file, won't overwrite unless option is flagged.

```python
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
>>> text_folder = TextFolder('some/path')
>>> print(text_folder)
some/path
```

---

#### TextFolder.text_files()

Load all .txt (or other types) in a folder as list of TextFile objects.

```python

>>> folder_files = TextFolder('some/path').text_files()
>>> for folder_file in folder_files:
...     print(folder_file.load())
Lorem ipsum dolor sit amet...

```

---

#### TextFolder.modify()

Opens every file and performs a callback function sent to it. Provides a fast
means of batch editing an entire folder of txt files. Returns a new TextFolder
linked with the modified copy.

```python

>>> # define a function which alters data as you wish
>>> def modify_record(record_data):
>>>     record_data = record_data.replace('\n', '')
>>>     return record_data

>>> # if you don't specify destination, a backup will be made
>>> options = {'destination': 'some/other-path'}

>>> # use TextFolder().modify, pass your function as 1st arg
>>> text_folder = TextFolder('some/path').modify(modify_record, options=options) # noqa
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
>>> # create column names and data set
>>> fake_fieldnames = ['id', 'text', 'notes']
>>> fake_data = [{
...         'id': '1',
...         'text': 'Lorem ipsum',
...         'notes': ''
...     }, {
...         'id': '2',
...         'text': 'dolor sit',
...         'notes': ''
...     }, {
...         'id': '3',
...         'text': 'amet.',
...         'notes': ''
...     }]
>>> # save to csv file
>>> csv_file = CSVFile('some/path.csv').save(fake_data, fieldnames=fake_fieldnames) # noqa
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

>>> # define a function which describes how to modify any given data row
>>> def modify_function(csv_record):
>>>     csv_record['text'] = 'Lorem ipsum dolor sit amet...'
>>>     csv_record['notes'] = 'Edited with dhelp'
>>>     return csv_record

>>> # pass a destination and your function as arguments to .modify()
>>> csv_file = CSVFile('some/path.csv')
>>> altered_csv_file = csv_file.modify('some/other-path.csv', modify_cb=modify_function)

>>> # .modify will return a new CSVFile object tied to the new location
>>> print(altered_csv_file)
/absolute/path/to/some/other-path.csv

```

---

#### CSVFile().column_to_txts()

Turns text data in a csv column into a series of .txt files. Text
is derived from a specified row (assumes 'text' if none specified).
To use another column to generate the filename for each record, use
filename_col, otherwise they will be numbered sequentially.

```python

>>> csv_file = CSVFile('some/path.csv')
>>> csv_file.column_to_txts('some/other-path', text_col='text', filename_col='id')

```
---

## Text Module

Module for text processing and natural language processing, primarily using
the natural language toolkit (nltk).

---

### **BaseText()**

Base class for all Text objects. Can be used on its own to perform a number
of operations, although it is best used with on of its language-specific
children.

```python

>>> from dhelp import BaseText

>>> base_text = BaseText('Lorem ipsum dolor sit amet...')
>>> print(base_text)
Lorem ipsum dolor sit amet...

```

**NOTE:** If you have not already downloaded nltk trainer packages, you must
do so before you can properly use nlp methods. Use the convenience method
below to launch the download interface. If you are on OSX/Windows, it will be a
GUI, if on Linux, a CLI.

```python
>>> BaseText('').setup()
```
---

#### BaseText().stringify()

Returns the text of this object as a pure string type.

```python

>>> base_text = BaseText('Lorem ipsum dolor sit amet...')
>>> stringified_text = base_text.stringify()
>>> print(type(stringified_text))
<class 'str'>


```

---

#### BaseText().rm_lines()

Gives a new version of the text with all endlines removed. Removes
any dashed line endings and rejoins split words.

```python

>>> base_text = BaseText('Lorem\nipsum do-\nlor sit amet....\n')
>>> modified_text = base_text.rm_lines()
>>> print(modified_text)
Lorem ipsum dolor sit amet...

```

---

#### BaseText().rm_nonchars()

Gives a new version of the text with only latin characters remaining.
Is overriden by child objects for languages using non latinate chars.

```python

>>> base_text = BaseText('1αLorem ipsum 2βdolor sit 3γamet...')
>>> modified_text = base_text.rm_nonchars()
>>> print(modified_text)
Lorem ipsum dolor sit amet...

```

---

#### BaseText().rm_edits()

Gives a new version with any text between editorial marks such as
brackets or parentheses removed. NOTE: May not work exactly as shown below,
the way this method deals with spaces inside or outside editorial marks needs
improvement.

```python

>>> base_text = BaseText('Lore[m i]psum {dolo}r sit a(met)...')
>>> modified_text = base_text.rm_edits()
>>> print(modified_text)
Lor psum r sit a...

```

---

#### BaseText().rm_spaces()

Gives a new version of the text with extra whitespace collapsed.

```python

>>> base_text = BaseText('Lorem   ipsum dolor  sit               amet...')
>>> modified_text = base_text.rm_spaces()
>>> print(modified_text)
Lorem ipsum dolor sit amet...

```

---

#### BaseText().rm_stopwords()

Given a list of words or phrases, gives new text with those phrases
removed.

```python

>>> stopwords = ['ipsum', 'sit']
>>> base_text = BaseText('Lorem ipsum dolor sit amet...')
>>> modified_text = base_text.rm_stopwords(stoplist=stopwords)
>>> print(modified_text)
Lorem dolor amet...

```

---

#### BaseText().lemmatize()

Gives a new version of the text in which every word is lemmatized. All verbs
are transformed into the first person singular present active, all nouns are
transformed into the singular masculine nominative, et.c. NOTE: May not work
exactly as below as this will be tweaked.

```python

>>> base_text = BaseText('The quick brown fox jumped over the lazy dog.') # noqa
>>> print(base_text.lemmatize())
'The quick brown fox jump over the lazy dog .'

```

---

#### BaseText().re_search()

Receives a [Regular Expression](https://regexr.com/) search pattern and returns
True/False if it matches.

```python

>>> base_text = BaseText('Lorem ipsum dolor sit amet...')
>>> print(base_text.re_search('Lorem ipsum'))
True
>>> print(base_text.re_search('Arma virumque cano'))
False

```

---

#### BaseText().tokenize()

Returns a tokenized list. By default returns list of words, but can also return
as a list of sentences.

```python

>>> base_text = BaseText('Lorem ipsum dolor sit amet. Consectetur adipiscing elit.')
>>> print(BaseText.tokenize())
['Lorem', 'ipsum', 'dolor', 'sit', 'amet', '.', 'Consectetur', 'adipiscing', 'elit', '.']
>>> print(BaseText.tokenize(mode='sentence'))
['Lorem ipsum dolor sit amet.', 'Consectetur adipiscing elit.']

```

---

#### BaseText().tag()

Returns list of words marked up with parts of speech. Each word is returned as
a 2-tuple, the first containing the word, the second with the parts of speech.

```python

>>> base_text = BaseText('They hated to think of sample sentences.')
>>> basic_tags = base_text.tag()
>>> print(basic_tags)
[('They', 'PRP'), ('hated', 'VBD'), ('to', 'TO'), ('think', 'VB'), ('of', 'IN'), ('sample', 'JJ'), ('sentences', 'NNS'), ('.', '.')]

```

---

#### BaseText().ngrams()

Returns a list of ngrams, each ngram represented as a tuple.

```python

>>> base_text = BaseText('They hated to think of sample sentences.')
>>> basic_ngrams = base_text.ngrams()
>>> print(basic_ngrams)
[('They', 'hated', 'to'), ('hated', 'to', 'think'), ('to', 'think', 'of'), ('think', 'of', 'sample'), ('of', 'sample', 'sentences'), ('sample', 'sentences', '.')]

```

---

#### BaseText().skipgrams()

Returns list of skipgrams, similar to ngram, but allows spacing between tokens.

```python

>>> base_text = BaseText('They hated to think of sample sentences.')
>>> basic_skipgrams = base_text.skipgrams()
>>> print(basic_skipgrams)
[('They', 'hated', 'to'), ('They', 'hated', 'think'), ('They', 'to', 'think'), ('hated', 'to', 'think'), ('hated', 'to', 'of'), ('hated', 'think', 'of'), ('to', 'think', 'of'), ('to', 'think', 'sample'), ('to', 'of', 'sample'), ('think', 'of', 'sample'), ('think', 'of', 'sentences'), ('think', 'sample', 'sentences'), ('of', 'sample', 'sentences'), ('of', 'sample', '.'), ('of', 'sentences', '.'), ('sample', 'sentences', '.')]

```
