#! /usr/bin/python3

import re
import argparse
from fpdf import FPDF

class MarkdownEngine:
    def __init__(self, outfile=None, infile=None):
        # set file for output
        if outfile is None:
            self.outfile = "out.pdf"
        else:
            self.set_outfile(outfile)

        # set file for input
        if infile is None:
            self.infile = "in.md"
        else:
            self.set_infile(infile)

        # create PDF object
        self.pdf = FPDF()


    # set the file for output
    # extensions are ignored and .pdf is assumed
    def set_outfile(self, outfile):
        name = re.search("^(.*)\..*", outfile)
        try:
            # append .pdf to filename
            self.outfile = name[1] + ".pdf"
        except TypeError:
            # if no extension provided, add one
            self.outfile = outfile + ".pdf"
        return self



    # set the file for input
    # extensions are ignored and .md is assumed
    def set_infile(self, infile):
        name = re.search("^(.*)\..*", infile)
        try:
            # append .md to filename
            self.infile = name[1] + ".md"
        except TypeError:
            # if no extension provided, add one
            self.infile = infile + ".md"
        return self




if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(description = "Generate flash cards from a Markdown file.")
    parser.add_argument("input", metavar='INFILE',
            help="Set the filename for input. Extensions are ignored and .md is assumed.")
    parser.add_argument("-o", "--out", metavar='OUTFILE', default="out.pdf",
            help="Set the filename for output. Extensions are ignored and .pdf is assumed. (Default: out.pdf)")
    args = parser.parse_args()

    # create markdown engine
    me = MarkdownEngine(outfile=args.out, infile=args.input)
