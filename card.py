class Card:
    def __init__(self, title_str = "Untitled"):
        self.title = Title(title_str)
        self.contents = []

    def add_content(self, content):
        self.contents.append(content)

    def to_pdf(self, pdf):
        pdf.add_page()
        # card title
        # TODO: change this to a header in a subclassed FPDF
        self.title.to_pdf(pdf)
        # card contents
        for content in self.contents:
            contents.to_pdf(pdf)

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
        pdf.multi_cell(0, 20, txt=card.title, align="C", border=1 if self.debug else 0)
        pdf.ln()
        pdf.set_font_size(old_font_size)

# a subtitle within a card
class Subtitle(CardContents):
    def to_pdf(self, pdf):
        old_font_size = pdf.font_size
        pdf.set_font_size(16)
        pdf.multi_cell(0, 16, txt=card.title, align="L", border=1 if self.debug else 0)
        pdf.set_font_size(old_font_size)

# a bulleted point
class BulletedPoint(CardContents):
    def __init__(self, text = "NULL", space_count = 0):
        super().__init__(text)
        self.spacing = "  " * space_count

    def to_pdf(self, pdf):
        # add spacing
        pdf.cell(pdf.get_string_width(self.spacing) + pdf.c_margin * 2, 14, txt=self.spacing, align="L", border=1 if self.debug else 0)
        # set bullet character
        bullet = chr(149)
        # draw bullet point
        pdf.cell(pdf.get_string_width(bullet) + pdf.c_margin * 2, 14, txt=bullet, align="L", border=1 if self.debug else 0)
        # draw text
        pdf.multi_cell(0, 14, txt=line, align="L", border=1 if self.debug else 0)
