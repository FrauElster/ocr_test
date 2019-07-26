import os
from fpdf import FPDF
import glob
from typing import List

FONTS = ['Courier', 'Arial', 'Times']


lorem = 'Lorem not available'
if os.path.exists('../lorem.txt'):
    lorem = open('../lorem.txt').read()
    lorem.encode('utf-8')


def main(min_font_size: int, max_font_size: int):
    assert min_font_size <= max_font_size
    special_fonts = get_special_fonts()
    print(special_fonts)
    for font_size in range(min_font_size, max_font_size + 1):

        for font in FONTS:

            pdf = FPDF('P', 'mm', 'A4')
            pdf.set_font(font)
            make_pdf(pdf, font, font_size)

        for special_font in special_fonts:
            pdf = FPDF('P', 'mm', 'A4')
            pdf.add_font(family=special_font, fname=special_font, uni=True)
            pdf.set_font(special_font)
            font_name = special_font.split('\\')[1]
            font_name = font_name.split('.')[0]
            make_pdf(pdf, font_name, font_size)


def get_special_fonts():
    special_fonts: List[str] = []
    for filename in glob.glob(os.path.join('../fonts', '*.ttf')):
        special_fonts.append(filename)
    return special_fonts


def make_pdf(pdf, font_name, font_size):
    if not os.path.isdir('../out_create'):
        os.mkdir('../out_create')

    title = f'{font_name}_{font_size}.pdf'
    pdf.add_page()
    pdf.set_font_size(font_size)
    pdf.multi_cell(150, 10, txt=lorem)
    pdf.output('../out_create/' + title)
    print(f'Created {title}')


if __name__ == '__main__':
    main(15, 25)