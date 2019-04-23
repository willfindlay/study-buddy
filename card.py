from fpdf import FPDF

class Cards(FPDF):
    def __init__(self, orientation = 'P', unit = 'mm', format='A4'):
        super().__init__(orientation, unit, format)
        self.cards = []
        self.curr_card = 0

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
            # increment card number
            self.curr_card += 1
        # write card to file
        self.output(filename)


class Card:
    def __init__(self, title_str = "Untitled"):
        self.title = Title(title_str)
        self.contents = []

    def add_content(self, content):
        self.contents.append(content)

    def to_pdf(self, pdf):
        # blank page with just title
        pdf.add_page()
        # page with information
        pdf.add_page()
        # card contents
        for content in self.contents:
            content.to_pdf(pdf)

class CardContents:
    def __init__(self, text = "NULL"):
        self.text = text

    def __str__(self):
        return self.text

    def to_pdf(self, pdf):
        raise NotImplementedError("This is an abstract method and has no business being called.")

# a card title
# TODO: change this to a header in a subclassed FPDF
class Title(CardContents):
    def to_pdf(self, pdf):
        old_font_size = pdf.font_size
        pdf.set_font_size(20)
        pdf.multi_cell(0, 20, txt=self.text, align="C", border=0)
        pdf.ln()
        pdf.set_font_size(old_font_size)

# a subtitle within a card
class Subtitle(CardContents):
    def to_pdf(self, pdf):
        old_font_size = pdf.font_size
        pdf.set_font_size(16)
        pdf.multi_cell(0, 16, txt=self.text, align="L", border=0)
        pdf.set_font_size(old_font_size)

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
        pdf.multi_cell(0, 14, txt=self.text, align="L", border=0)

    def draw_point(self, pdf, number=1):
        # set bullet character
        bullet = "".join(["  ",chr(149)])
        pdf.cell(pdf.get_string_width("99.") + 2 + pdf.c_margin * 2, 14, txt=bullet, align="L", border=0)

# a numbered point
class NumberedPoint(BulletedPoint):
    def __init__(self, text="NULL", level=0, number=1):
        super().__init__(text, level)
        self.number = number

    def draw_point(self, pdf, number=1):
        # set number string
        numstr = f"{number:2}. "
        pdf.cell(pdf.get_string_width("99.") + 2 + pdf.c_margin * 2, 14, txt=numstr, align="L", border=0)
