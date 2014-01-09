#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import codecs
from nltk.tag.util import str2tuple


def main():
    parser = argparse.ArgumentParser(description="""\
    Convert pos tagged file to whitespace tokenized file.
    """)
    parser.add_argument("-I", "--input", required=True, help="input file")
    parser.add_argument("-O", "--output", required=True, help="output file")
    args = parser.parse_args()

    if args.input and args.output:
        with codecs.open(args.output, "w", "utf-8") as out:
            for sentence in codecs.open(args.input, "r", "utf-8"):
                tokens = [str2tuple(token) for token in sentence.split()]
                out.write(u"{0}\n".format(" ".join([word for word, tag
                                                    in tokens])))
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

