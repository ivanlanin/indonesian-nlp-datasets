#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import codecs
from collections import Counter, defaultdict
from nltk.tag.util import str2tuple, tuple2str
from tabulate import tabulate


def main():
    parser = argparse.ArgumentParser(description="""\
    Creates tag statistics.
    """)
    parser.add_argument("-I", "--input", required=True, help="input file")
    parser.add_argument("-O", "--output", required=True, help="output file")
    args = parser.parse_args()

    if args.input and args.output:
        with codecs.open(args.output, "w", "utf-8") as out:
            word_tags = defaultdict(set)
            word_counter = Counter()
            wordtag_counter = Counter()
            for sentence in codecs.open(args.input, "r", "utf-8"):
                tokens = [str2tuple(token) for token in sentence.split()]
                for word, tag in tokens:
                    word_tags[word].add(tag)
                    word_counter[word] += 1
                    wordtag_counter[tuple2str((word, tag))] += 1
            result = {"word": [], "count": [], "tags": []}
            for word, count in word_counter.most_common():
                result["word"].append(word)
                result["count"].append(count)
                tagged = set()
                for tag in word_tags[word]:
                    tagged.add(tuple2str((word, tag)))
                result["tags"].append(", ".join([":".join([str(wordtag_counter[t]), t]) for t in tagged]))
            out.write(u"{0}".format(tabulate(result, headers="keys", tablefmt="grid")))
    else:
        print parser.print_help()


if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt, e:
        raise e
    except SystemExit, e:
        raise e
    except Exception, e:
        print e
        import traceback
        traceback.print_exc()
        sys.exit(1)

