#! /usr/bin/python3

import re
import argparse
from fpdf import FPDF

DEBUG = False

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

        # create the initial pdf
        self.reset_pdf()

        # set cards array to empty
        self.cards = []


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



    # reset the PDF object
    def reset_pdf(self):
        # create PDF object
        self.pdf = FPDF("P", "pt", (360,216))
        self.pdf.set_font("Arial", size=12)
        self.pdf.set_margins(30,30)
        return self



    # generate the flashcards
    def generate_flashcards(self):
        # prints a big title for a section
        def print_section(title):
            self.pdf.add_page()
            self.pdf.set_font_size(36)
            self.pdf.multi_cell(0, 120, txt=title, align="C", border=1 if DEBUG else 0)
            self.pdf.set_font_size(12)

        # print the title of a card
        def print_title(card):
            self.pdf.add_page()
            self.pdf.set_font_size(16)
            self.pdf.multi_cell(0, 16, txt=card.title, align="C", border=1 if DEBUG else 0)
            self.pdf.ln()
            self.pdf.set_font_size(12)

        # print the actual card itself
        def print_card(card):
            # set bullet point character
            bullet = chr(149)
            # add page without answers
            print_title(card)
            # add page with answers
            for points in range(len(card.contents)):
                print_title(card)
                for i in range(points+1):
                    line = card.contents[i]
                    # draw bullet point
                    self.pdf.cell(self.pdf.get_string_width(bullet) + self.pdf.c_margin * 2, 12, txt=bullet, align="L", border=1 if DEBUG else 0)
                    # draw text
                    self.pdf.multi_cell(0, 12, txt=line, align="L", border=1 if DEBUG else 0)

        self.parse_cards()
        self.reset_pdf()
        print_section("Section")
        # FIXME: this should be done by card in self.cards
        print_card(Card("test title", ["test contents","test contents","asdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasd"]))
        self.pdf.output(self.outfile)



    def parse_cards(self):
        # TODO: implement me! should parse cards from input file
        pass



class Card:
    def __init__(self, title=None, contents=None):
        # set title
        if title is None:
            self.title = "Untitled"
        else:
            self.title = title

        # set contents
        if contents is None:
            self.contents = []
        else:
            if type(contents) != list:
                raise Exception("Conents must be a list")
            self.contents = contents



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

    card = Card(contents=[])

    me.generate_flashcards()
