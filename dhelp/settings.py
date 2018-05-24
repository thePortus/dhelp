LANGUAGES = [
    'english',
    'latin',
    'ancient greek',
]

DELIMITERS = [
    ',',
    ';',
    '\t',
]

NLTK_PACKAGES = {
    'all': [
        ('punkt', ['tokenizers', 'punkt.zip']),
        ('verbnet', ['corpora', 'verbnet.zip']),
        ('wordnet', ['corpora', 'wordnet.zip']),
        ('large_grammars', ['grammars', 'large_grammars.zip']),
        ('large_grammars', ['grammars', 'large_grammars.zip']),
        (
            'averaged_perceptron_tagger',
            ['taggers', 'averaged_perceptron_tagger.zip']
        ),
        (
            'maxent_treebank_pos_tagger',
            ['taggers', 'maxent_treebank_pos_tagger.zip']
        ),
        ('maxent_ne_chunker', ['chunkers', 'maxent_ne_chunker.zip']),
        ('universal_tagset', ['taggers', 'universal_tagset.zip']),
    ],
    'english': [
        ('words', ['corpora', 'words.zip']),
        ('sample_grammars', ['grammars', 'sample_grammars.zip']),
        ('book_grammars', ['grammars', 'book_grammars.zip']),
        ('perluniprops', ['misc', 'perluniprops.zip'])
    ],
    'spanish': [
        ('spanish_grammars', ['grammars', 'spanish_grammars.zip'])
    ],
    'basque': [
        ('basque_grammars', ['grammars', 'basque_grammars.zip'])
    ]
}

# TODO: Change CLTK setup so it expects path segments like NLTK settings
CLTK_PACKAGES = {
    'greek': [
        ('greek_software_tlgu', 'software/greek_software_tlgu'),
        ('greek_proper_names_cltk', 'lexicon_greek_proper_names_cltk'),
        ('greek_models_cltk', 'models/greek_models_cltk'),
        ('greek_treebank_perseus', 'treebank/greek_treebank_perseus'),
        ('greek_lexica_perseus', 'lexicon/greek_lexica_perseus'),
        (
            'greek_training_set_sentence_cltk',
            'training_set/greek_training_set_sentence_cltk'
        ),
        ('greek_word2vec_cltk', 'lexicon/greek_word2vec_cltk'),
    ],
    'latin': [
        ('latin_treebank_perseus', 'treebank/latin_treebank_perseus'),
        ('latin_proper_names_cltk', 'lexicon/latin_proper_names_cltk'),
        ('latin_models_cltk', 'models/latin_models_cltk'),
        ('latin_pos_lemmata_cltk', 'lemma/latin_pos_lemmata_cltk'),
        (
            'latin_treebank_index_thomisticus',
            'treebank/latin_treebank_index_thomisticus'
        ),
        ('latin_lexica_perseus', 'lexicon/latin_lexica_perseus'),
        (
            'latin_training_set_sentence_cltk',
            'training_set/latin_training_set_sentence_cltk'
        ),
        ('latin_word2vec_cltk', 'models/latin_word2vec_cltk'),
    ]
}

ENCODINGS = [
    ('ascii'),
    ('big5'),
    ('big5khscs'),
    ('cp037'),
    ('cp273'),
    ('cp424'),
    ('cp437'),
    ('cp500'),
    ('cp720'),
    ('cp737'),
    ('cp775'),
    ('cp850'),
    ('cp852'),
    ('cp855'),
    ('cp856'),
    ('cp857'),
    ('cp858'),
    ('cp860'),
    ('cp861'),
    ('cp862'),
    ('cp863'),
    ('cp864'),
    ('cp865'),
    ('cp866'),
    ('cp869'),
    ('cp874'),
    ('cp875'),
    ('cp932'),
    ('cp949'),
    ('cp950'),
    ('cp1006'),
    ('cp1026'),
    ('cp1125'),
    ('cp1140'),
    ('cp1250'),
    ('cp1251'),
    ('cp1252'),
    ('cp1254'),
    ('cp1255'),
    ('cp1256'),
    ('cp1257'),
    ('cp1258'),
    ('cp65001'),
    ('euc_jp'),
    ('euc_jis_2004'),
    ('euc_jisx0213'),
    ('euc_kr'),
    ('gb2312'),
    ('gbk'),
    ('gb18030'),
    ('hz'),
    ('iso2022_jp'),
    ('iso2022_jp_1'),
    ('iso2022_jp_2'),
    ('iso2022_jp_2004'),
    ('iso2022_jp_3'),
    ('iso2022_jp_exit'),
    ('iso2022_kr'),
    ('latin_1'),
    ('iso8859_2'),
    ('iso8859_3'),
    ('iso8859_4'),
    ('iso8859_5'),
    ('iso8859_6'),
    ('iso8859_7'),
    ('iso8859_8'),
    ('iso8859_9'),
    ('iso8859_10'),
    ('iso8859_11'),
    ('iso8859_13'),
    ('iso8859_14'),
    ('iso8859_15'),
    ('iso8859_16'),
    ('johab'),
    ('koi8_r'),
    ('koi8_t'),
    ('koi8_u'),
    ('kz1048'),
    ('mac_cyrillic'),
    ('mac_greek'),
    ('mac_iceland'),
    ('mac_latin2'),
    ('mac_roman'),
    ('mac_turkish'),
    ('ptcp154'),
    ('shift_jis'),
    ('shift_jis_2004'),
    ('shift_jisx0213'),
    ('utf_32'),
    ('utf_32_be'),
    ('utf_32_le'),
    ('utf_16'),
    ('utf_16_be'),
    ('utf_16_le'),
    ('utf_7'),
    ('utf_8'),
    ('utf_8_sig'),
]
