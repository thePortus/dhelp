try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    from distutils.core import setup
    from distutils.core import find_packages

config = {
    'name': 'dhelp',
    'author': 'David J. Thomas',
    'author_email': 'dave.a.base@gmail.com',
    'description': """DH Python tools for scraping web pages, pre-processing
    data, and performing nlp analysis quickly.""",
    'version': '0.0.5',
    'LICENSE': 'MIT',
    'long_description': """Students often see great potential in Python for
    historical analysis. But, before they see real payoff they often face too
    many hurdles to overcome in the space of a single semester. dhelp is a tool
    to allow students to quickly get to performing quick file operations, data
    manipulations, and even text analysis.""",
    'url': 'https://github.com/thePortus/dhelp',
    'download_url': 'https://github.com/thePortus/dhelp/archive/master.zip',
    'packages': find_packages(),
    'install_requires': [
        'beautifulsoup4==4.6.0',
        'certifi==2022.12.7',
        'chardet==3.0.4',
        'idna==2.6',
        'nltk==3.2.5',
        'requests==2.18.4',
        'six==1.11.0',
        'urllib3==1.22',
    ],
    'keywords': [
        'digital-humanities',
        'digital-history',
        'digital-analysis',
        'text-processing',
        'text-analysis',
        'nltk',
        'nlp',
        'natural-language-processing',
        'greek',
        'latin'
    ],
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Topic :: Sociology :: History',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Linguistic',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Natural Language :: Latin',
        'Natural Language :: Greek',
    ],
}

setup(**config)
