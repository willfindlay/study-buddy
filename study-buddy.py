#! /usr/bin/python3

import re
import argparse
from fpdf import FPDF

class MarkdownEngine:
    def __init__(self, outfile="flashcards.pdf", infile="in.md", debug=False):
        # set file for output
        self.set_outfile(outfile)

        # set file for input
        self.set_infile(infile)

        # set debug mode
        self.debug = debug

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
        self.pdf = FPDF("L", "pt", (360,576))
        self.pdf.set_font("Arial", size=12)
        self.pdf.set_margins(40,30)
        return self



    # generate the flashcards
    def generate_flashcards(self):
        # prints a big title for a section
        def print_section(title):
            self.pdf.add_page()
            self.pdf.set_font_size(20)
            self.pdf.multi_cell(0, 20, txt=title, align="C", border=1 if self.debug else 0)
            self.pdf.set_font_size(12)

        # print the title of a card
        def print_title(card):
            self.pdf.add_page()
            self.pdf.set_font_size(16)
            self.pdf.multi_cell(0, 16, txt=card.title, align="C", border=1 if self.debug else 0)
            self.pdf.ln()
            self.pdf.set_font_size(12)

        # print the actual card itself
        def print_card(card):
            # set bullet point character
            bullet = chr(149)
            # add page without answers
            print_title(card)
            # add page with answers
            print_title(card)
            for i in range(len(card.contents)):
                line = card.contents[i]
                spacing = card.spacing[i]
                # add spacing
                self.pdf.cell(self.pdf.get_string_width(spacing) + self.pdf.c_margin * 2, 14, txt=spacing, align="L", border=1 if self.debug else 0)
                # draw bullet point
                self.pdf.cell(self.pdf.get_string_width(bullet) + self.pdf.c_margin * 2, 14, txt=bullet, align="L", border=1 if self.debug else 0)
                # draw text
                self.pdf.multi_cell(0, 14, txt=line, align="L", border=1 if self.debug else 0)

        self.parse_cards()
        self.reset_pdf()

        # print sections and cards
        for card in self.cards:
            if card.section == True:
                print_section(card.title)
            else:
                print_card(card)

        self.pdf.output(self.outfile)



    def parse_cards(self):
        # reset cards
        self.cards = []

        # read in card from the file
        with open(self.infile) as f:
            # set card to None for now
            card = None
            for line in f:
                # attempt to find section, card, or line
                section = re.match(r"^\s*#\s+(.*)", line)
                cardtitle = re.match(r"^\s*##\s+(.*)", line)
                text = re.match(r"^(\s*)(?:[\-\*\+]|1\.)\s+(.*)", line)

                # try to add a section
                try:
                    section[1]

                    card = Card(title=section[1], section=True)
                    self.cards.append(card)
                    card = None

                    continue
                except TypeError:
                    pass

                # try to add a card
                try:
                    cardtitle[1]

                    if card is not None:
                        self.cards.append(card)
                    card = Card(title=cardtitle[1])

                    continue
                except TypeError:
                    pass

                # try to add a bullet point
                try:
                    print(text[1], text[2])
                    text[2]

                    if card is not None:
                        card.add_point(text[1], text[2])

                    continue
                except TypeError:
                    pass

            # append last card
            if card is not None:
                self.cards.append(card)



class Card:
    def __init__(self, title="Untitled", section=False):
        # set title
        self.title = title

        # set contents
        self.contents = []

        # set spacing
        self.spacing = []

        # set section
        self.section = section



    # add a bullet point to card contents
    def add_point(self, spacing, point):
        self.spacing.append(spacing)
        self.contents.append(str(point))



if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(description = "Generate flash cards from a Markdown file.")
    parser.add_argument("input", metavar='INFILE',
            help="Set the filename for input. Extensions are ignored and .md is assumed.")
    parser.add_argument("-o", "--out", metavar='OUTFILE', default="flashcards.pdf",
            help="Set the filename for output. Extensions are ignored and .pdf is assumed. (Default: flashcards.pdf)")
    args = parser.parse_args()

    # create markdown engine
    me = MarkdownEngine(outfile=args.out, infile=args.input, debug=False)

    # generate flashcards
    me.generate_flashcards()
