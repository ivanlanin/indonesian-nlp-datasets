Indonesian POS Tag Datasets
===========================

**Note: This is a work in progress dataset.**

## Tagset

This dataset is tagged using [Universal Part-of-Speech tagset](https://code.google.com/p/universal-pos-tags/).

Classes used are:

| Tag   | Notes                                     |
| ----- | ----------------------------------------- |
| .     | Punctuation marks                         |
| ADJ   | Adjectives                                |
| ADP   | Prepositions and postpositions            |
| ADV   | Adverbs                                   |
| CONJ  | Conjunctions                              |
| DET   | Determiners and articles                  |
| NOUN  | Nouns                                     |
| NUM   | Numerals                                  |
| PRON  | Pronouns                                  |
| PRT   | Particles                                 |
| VERB  | Verbs                                     |
| X     | Abbreviations, foreign words, typos, etc. |


## Statistics

The `../utils/tagstat.py` script will show the following statistics about a tagged corpus.

* total number of words
* words
* tags and the number of each tag occurs ('*' mark: tag is not in Google translate tag list)
* list of tags for each word according to Google Translate

Example:

To generate all entries:

    python ../utils/tagstat.py -L lexicon-id.json -I id-news.pos -O id-news-stat.md

To generate maximum `NUM` entires:

    python ../utils/tagstat.py -L lexicon-id.json -I id-news.pos -O id-news-stat.md -M 500

