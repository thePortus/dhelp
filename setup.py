try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': "dhelp",
    'packages': [
        "src",
        "src.files",
        "src.text",
        "src.web"
    ],
    'install_requires': ["nltk", "BeautifulSoup4", "requests"],
    'version': "0.0.0",
    'description': "Helper objects for DH Students",
    'author': "David J. Thomas",
    'author_email': "dave.a.base@gmail.com",
    'url': "https://github.com/thePortus/arakhne",
    'download_url': "https://github.com/thePortus/dhelp/archive/master.zip",
    'keywords': [
        "digital humanities",
        "nltk",
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
