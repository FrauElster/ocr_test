import os
from fpdf import FPDF
import glob
from typing import List
from .FileHandler import FileHandler

FONTS = ['Courier', 'Arial', 'Times']


def main(min_font_size: int, max_font_size: int):
    assert min_font_size <= max_font_size
    lorem: str = FileHandler.load_file(FileHandler.get_path('../lorem.txt'))
    create_pdfs(min_font_size, max_font_size, lorem)
    FileHandler.delete_with_ending('../fonts', 'pkl')


def create_pdfs(min_font_size: int, max_font_size: int, text: str):
    special_fonts = get_special_fonts()

    for font_size in range(min_font_size, max_font_size + 1):

        for font in FONTS:
            pdf = FPDF('P', 'mm', 'A4')
            pdf.set_font(font)
            make_pdf(pdf, font, font_size, text)

        for special_font in special_fonts:
            pdf = FPDF('P', 'mm', 'A4')
            pdf.add_font(family=special_font, fname=special_font, uni=True)
            print(f'Special Font: {special_font}')
            pdf.set_font(special_font)
            font_name = special_font.split('/')[-1]
            font_name = font_name.split('.')[0]
            make_pdf(pdf, font_name, font_size, text)


def get_special_fonts():
    os.environ['FPDF_FONTPATH'] = FileHandler.get_path('../fonts')
    os.environ['FPDF_CACHE_MODE'] = FileHandler.get_path('1')
    special_fonts: List[str] = []
    #    for filename in glob.glob(os.path.join(FileHandler.get_path('../fonts'), '*.ttf')):
    for filename in glob.glob(os.path.join(FileHandler.get_path('../fonts'), '*.ttf')):
        print(f'DEBUG: {filename}')
        special_fonts.append(filename)
    return special_fonts


def make_pdf(pdf, font_name: str, font_size: int, lorem: str):
    dir_path = FileHandler.get_path('../out_create')
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    title = f'{font_name}_{font_size}.pdf'
    pdf.add_page()
    pdf.set_font_size(font_size)
    pdf.multi_cell(150, 10, txt=lorem)

    pdf.output(f'{dir_path}/{title}')
    print(f'Created {title}')
