#! /usr/bin/python3

import re
import argparse

class MarkdownEngine:
    def __init__(self, outfile=None):
        # set file for output
        if outfile is None:
            self.outfile = "out.pdf"
        else:
            self.set_outfile(outfile)

    def set_outfile(self, outfile):
        name = re.search("^(.*)\..*", outfile)
        try:
            # append .pdf to filename
            self.outfile = name[1] + ".pdf"
        except TypeError:
            # if no extension provided, add one
            self.outfile = outfile + ".pdf"
        return self

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(description = "Generate flash cards from a Markdown file.")
    parser.parse_args()

    me = MarkdownEngine(outfile="test2.pdf")

    print(me.outfile)
