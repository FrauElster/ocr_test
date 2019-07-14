import os
from fpdf import FPDF

FONTS = ['Courier', 'Arial', 'Times']
SPECIAL_FONTS = ['CaviarDreams', 'Champagne & Limousines', 'Roboto-Black', 'vogue']

MIN_FONT_SIZE = 5
MAX_FONT_SIZE = 30


lorem = 'Lorem not available'
if os.path.exists('../lorem.txt'):
    lorem = open('../lorem.txt').read()
    lorem.encode('utf-8')


def main():
    for font_size in range(MIN_FONT_SIZE, MAX_FONT_SIZE + 1):
        for font in FONTS:

            pdf = FPDF('P', 'mm', 'A4')
            make_pdf(pdf, font, font_size)

        for special_font in SPECIAL_FONTS:
            pdf = FPDF('P', 'mm', 'A4')
            pdf.add_font(family=special_font, fname=f'../fonts/{special_font}.ttf', uni=True)
            make_pdf(pdf, special_font, font_size)


def make_pdf(pdf, font, font_size):
    title = f'{font}_{font_size}.pdf'
    pdf.add_page()
    pdf.set_font(font)
    pdf.set_font_size(font_size)
    pdf.multi_cell(150, 10, txt=lorem)
    print(title)
    pdf.output('../out/' + title)


if __name__ == '__main__':
    main()