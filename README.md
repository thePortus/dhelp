# dhelp

---

[![Build Status](https://travis-ci.org/thePortus/dhelp.svg?branch=master)](https://travis-ci.org/thePortus/dhelp) [![Coverage Status](https://coveralls.io/repos/github/thePortus/dhelp/badge.svg?branch=master)](https://coveralls.io/github/thePortus/dhelp?branch=master)

---

[David J. Thomas](mailto:dave.a.base@gmail.com), [thePortus.com](http://thePortus.com)<br>
Instructor of Ancient History and Digital Humanities, [University of South Florida](https://github.com/usf-portal)

---

Helper objects for various Digital Humanities related tasks. Contains modules
to work with text files/folders, CSVs, webpages, and perform natural language
processing.

---

# Installation

```
pip install dhelp
```

---

# Examples

---

## Text Files

Load and save plain text data to/from files with TextFile.

```python
from dhelp import TextFile

# load file as a string
file_data = TextFile('some/path.txt').load()
# remove all endlines
file_data = file_data.replace('\n')
# save altered text, specifying the overwrite option
TextFile('some/path.txt').save(file_data, options={'overwrite':  True})

```

---

## Text Folders

Modify entire folders of plain text data easily with TextFolder. You can use
.load() to get a list of TextFile objects, each one already linked to the
location of a file in the folder. Better yet, to streamline text processing,
you can use .modify(). Once you define a function showing how to alter the data
of a single file, you can then load, modify, and save every single file in
a folder in a single line of code.

```python
from dhelp import TextFolder

# load .txts in folder as list of TextFile objs, each linked to file loc
folder_files = TextFolder('some/folder').load()
# loop through each TextFile object, load data and print
for folder_file in folder_files:
    print(folder_file.load())
```

Setting options...

```python
# options dict, specifying all possible options, including output dir
options_settings = {
    'encoding': 'utf-8',
    'extensions': ['txt', 'html', 'rtf']
}
# pass the dict as the options argument
TextFolder('some/folder').load(options=options_settings)
```

Modify all files, simplified

```python
# make a function defining how to modify the data of a single record
# function must have single arg (e.g. record_data), alter it, and return it
def modify_record(record_data):
    # remove all endlines
    record_data = record_data.replace('\n', '')
    # return altered data
    return record_data

# if you don't specify destination, a backup will automatically be created
options_settings = {'destination': 'some/other-folder'}

# use TextFolder().modify, pass your function as 1st arg
# TextFolder will then load, modify, and save each file automatically!
TextFolder('some/folder').modify(modify_record, options=options_settings)

```

---

## CSV Files

```python

```

---

## Web Pages

```python

```

---

## Natural Language Processing

```python

```
