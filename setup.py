try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': "dhelp",
    'packages': [
        "dhelp"
    ],
    'install_requires': [
        "nltk",
        "BeautifulSoup4",
        "requests"
    ],
    'version': "0.0.1",
    'description': """Utility tools for scraping, processing, and analyzing
    data for DH students.""",
    'author': "David J. Thomas",
    'author_email': "dave.a.base@gmail.com",
    'url': "https://github.com/thePortus/arakhne",
    'download_url': "https://github.com/thePortus/dhelp/archive/master.zip",
    'keywords': [
        "digital-humanities",
        "digital-history",
        "digital-analysis",
        "text-processing",
        "text-analysis",
        "nltk",
        "nlp",
        "natural-language-processing"
    ],
    'classifiers': [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Sociology :: History"
    ],
}

setup(**config)
