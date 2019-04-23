#! /usr/bin/python3

import re
import argparse
from card import *
from unit_test import test_cards

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
        self.pdf = Cards("L", "pt", (360,576))
        self.pdf.set_font("Arial", size=12)
        self.pdf.set_margins(40,30)
        return self

    # generate the flashcards
    def generate_flashcards(self):
        self.parse_cards()
        self.reset_pdf()

        for card in self.cards:
            print("exporting a card")
            self.pdf.add_card(card)

        self.pdf.export(self.outfile)

    def parse_cards(self):
        # reset cards
        self.cards = []

        # read in card from the file
        with open(self.infile) as f:
            # set card to None for now
            card = None
            # initialize point number for numbered points
            point_number = 1
            for line in f:
                # attempt to find section, card, or line
                cardtitle = re.match(r"^\s*#\s+(.*)", line)
                subtitle = re.match(r"^\s*##\s+(.*)", line)
                # TODO: match me
                subsubtitle = re.match(r"^\s*###\s+(.*)", line)
                # TODO: match me
                subsubsubtitle = re.match(r"^\s*#####*\s+(.*)", line)
                # TODO: match me
                bulleted = re.match(r"^(\s*)(?:[\-\*\+])\s+(.*)", line)
                # TODO: match me
                numbered = re.match(r"^(\s*)(?:\d\.|\d\)|\(\d\))\s+(.*)", line)

                # try to add a card
                try:
                    cardtitle[1]

                    print("found a card")

                    card = Card(title_str=cardtitle[1])
                    self.cards.append(card)

                    continue
                except TypeError:
                    pass

                # try to add a subtitle
                try:
                    subtitle[1]

                    content = Subtitle(text=subtitle[1])
                    if card is not None:
                        card.add_content(content)

                    continue
                except TypeError:
                    pass

                # TODO: implement subsub titles and subsubsub titles

                # try to add a bulleted point
                try:
                    bulleted[1]

                    content = BulletedPoint(text=bulleted[2], level=len(bulleted[1]))
                    if card is not None:
                        card.add_content(content)

                    continue
                except TypeError:
                    pass

                # try to add a numbered point
                try:
                    numbered[1]

                    content = NumberedPoint(text=numbered[2], number=point_number, level=len(numbered[1]))
                    if card is not None:
                        card.add_content(content)
                        point_number += 1

                    continue
                except TypeError:
                    point_number = 1

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
