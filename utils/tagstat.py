#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import codecs
import json
from collections import Counter, defaultdict
from nltk.tag.util import str2tuple, tuple2str
from tabulate import tabulate


def main():
    parser = argparse.ArgumentParser(description="""\
    Creates tag statistics.
    """)
    parser.add_argument("-I", "--input", required=True, help="input file")
    parser.add_argument("-O", "--output", required=True, help="output file")
    parser.add_argument("-L", "--lexicon", required=True, help="lexicon file")
    parser.add_argument("-M", "--max", help="maximum output")
    args = parser.parse_args()

    if args.input and args.output and args.lexicon:
        lexicon = json.load(open(args.lexicon))
        with codecs.open(args.output, "w", "utf-8") as out:
            wt = defaultdict(set)
            wc = Counter()
            wtc = Counter()

            for sentence in codecs.open(args.input, "r", "utf-8"):
                tokens = [str2tuple(token) for token in sentence.split()]

                for word, tag in tokens:
                    wt[word].add(tag)
                    wc[word] += 1
                    wtc[tuple2str((word, tag))] += 1

            r = {"Count": [],
                 "Words": [],
                 "Found": [],
                 "Lexicon": []}

            for word, count in wc.most_common(int(args.max) or None):
                r["Words"].append(word)
                r["Count"].append(count)
                tg = set()

                for tag in wt[word]:
                    t = tuple2str((word, tag))
                    in_lex = ""
                    if lexicon.get(word.lower()):
                        if tag not in lexicon.get(word.lower()):
                            in_lex = "*"
                    tg.add((tag + in_lex, wtc[t]))

                tg = sorted(tg, key=lambda k: k[1], reverse=True)
                r["Found"].append(", ".join([u"{0} ({1})".format(x, y)
                                                       for x, y in tg]))
                if lexicon.get(word.lower()):
                    r["Lexicon"].append(", ".join(lexicon.get(word.lower())))
                else:
                    r["Lexicon"].append("")
            out.write(u"{0}".format(tabulate(r,
                                             headers="keys",
                                             tablefmt="pipe")))
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

