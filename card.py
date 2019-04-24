from fpdf import FPDF

class Cards(FPDF):
    def __init__(self, orientation = 'P', unit = 'mm', format='A4'):
        super().__init__(orientation, unit, format)
        self.cards = []
        self.curr_card = 0
        # we do not want to auto page break
        self.set_auto_page_break(False)

    def add_card(self, card):
        self.cards.append(card)

    def header(self):
        self.set_font("Arial")
        try:
            self.cards[self.curr_card].title.to_pdf(self)
        except IndexError:
            return

    def export(self,filename):
        # draw each card
        for card in self.cards:
            # draw card
            card.to_pdf(self)
            # check to see if we went over the page; if so, print a warning
            page_height = self.fw_pt if self.def_orientation == "L" else self.fh_pt
            if self.get_y() > page_height:
                print(f"WARNING: Card \"{card.title.text}\" is too long. Output truncated.")
            # increment card number
            self.curr_card += 1
        # write card to file
        self.output(filename)


class Card:
    def __init__(self, title_str = "Untitled"):
        self.title = Title(title_str)
        self.contents = []
        self.printed = []

    def add_content(self, content):
        self.contents.append(content)

    def soft_page_break(self, pdf):
        pdf.add_page()
        for printed in self.printed:
            printed.to_pdf(pdf)

    def to_pdf(self, pdf):
        # blank page with just title
        pdf.add_page()
        # page with information
        pdf.add_page()
        # card contents
        for content in self.contents:
            # insert an extra page break before printing subtitles
            # but only if they are not the first subtitles
            if type(content) is Subtitle and not content.first:
                self.soft_page_break(pdf)

            self.printed.append(content)
            content.to_pdf(pdf)

            # insert an extra page break after printing subtitles
            if type(content) is Subtitle:
                self.soft_page_break(pdf)

class CardContents:
    def __init__(self, text = "NULL"):
        self.text = text

    def __str__(self):
        return self.text

    def to_pdf(self, pdf):
        raise NotImplementedError("This is an abstract method and has no business being called.")

# a card title
class Title(CardContents):
    def to_pdf(self, pdf):
        pdf.set_font("Arial","B",20)
        pdf.multi_cell(0, 20, txt=self.text, align="C", border=0)
        pdf.set_font("Arial","",12)
        pdf.ln(12)

# a subtitle within a card
class Subtitle(CardContents):
    def __init__(self, text = "NULL", first=False):
        super().__init__(text)
        self.first = first

    def to_pdf(self, pdf):
        pdf.set_font("Arial","B",16)
        # add a blank space if necessary
        if not self.first:
            pdf.ln(12)
        pdf.multi_cell(0, 16, txt=self.text, align="L", border=0)
        pdf.set_font("Arial","",12)

# a subsubtitle within a card
class Subsubtitle(CardContents):
    def to_pdf(self, pdf):
        pdf.set_font("Arial","B",14)
        pdf.multi_cell(0, 14, txt=self.text, align="L", border=0)
        pdf.set_font("Arial","",12)

# a subsubsubtitle within a card
class Subsubsubtitle(CardContents):
    def to_pdf(self, pdf):
        pdf.set_font("Arial","B",12)
        pdf.multi_cell(0, 12, txt=self.text, align="L", border=0)
        pdf.set_font("Arial","",12)

# a bulleted point
class BulletedPoint(CardContents):
    def __init__(self, text = "NULL", level = 0):
        super().__init__(text)
        self.spacing = "    " * level
        self.number = 0

    def to_pdf(self, pdf):
        # save old font and change family to Courier
        old_font = pdf.font_family
        pdf.set_font("Courier")
        # add spacing
        pdf.cell(pdf.get_string_width(self.spacing) + pdf.c_margin * 2, 14, txt=self.spacing, align="L", border=0)
        # draw bullet point
        self.draw_point(pdf, self.number)
        # return old font
        pdf.set_font(old_font)
        # draw text
        pdf.multi_cell(0, 12, txt=self.text, align="L", border=0)

    def draw_point(self, pdf, number=1):
        # set bullet character
        bullet = "".join(["  ",chr(149)])
        # we want this to be wide enough to match NumberedPoint
        pdf.cell(pdf.get_string_width("99.") + 2 + pdf.c_margin * 2, 14, txt=bullet, align="L", border=0)

# a numbered point
class NumberedPoint(BulletedPoint):
    def __init__(self, text="NULL", level=0, number=1):
        super().__init__(text, level)
        self.number = number

    def draw_point(self, pdf, number=1):
        # set number string
        numstr = f"{number:2}. "
        # we want this to be wide enough to fit up to 99 numbers
        pdf.cell(pdf.get_string_width("99.") + 2 + pdf.c_margin * 2, 14, txt=numstr, align="L", border=0)

# a plaintext paragraph
class Text(CardContents):
    def to_pdf(self, pdf):
        pdf.set_font_size(12)
        pdf.multi_cell(0, 12, txt=self.text, align="L", border=0)
        pdf.set_font_size(12)
