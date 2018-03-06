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

The text module attaches mutiple methods for text cleaning/analysis that can
be easily accessed. Use one of the Text classes to get a string-like object
that comes with many convenient cleaning/nlp methods attached. You can chain
any of the string transformation methods to perform many text operations at
once.

```python

# TODO: Text module examples coming soon. Check out the [documentation](http://dhelp.readthedocs.io) instead.

```
