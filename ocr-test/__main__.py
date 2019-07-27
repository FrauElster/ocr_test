import glob
import os
import click

from . import create_pdf, evaluate
from .FileHandler import FileHandler


@click.group()
def main():
    pass


@main.command()
@click.option('--max', 'max_font_size', type=int, required=True, help="Max font size")
@click.option('--min', 'min_font_size', type=int, required=True, help="Min font size")
def create(min_font_size, max_font_size):
    create_pdf.main(min_font_size, max_font_size)


@main.command()
@click.option('--path', type=str, default='../out_create/', help="Path to PDFs")
def eval(path: str):
    evaluate.main(path)


@main.command()
@click.option('--type', required=True, type=click.Choice(['txt', 'pdf']))
def delete(type: str):
    if type == 'txt':
        FileHandler.delete_with_ending('../out_create/', '*.txt')
    elif type == 'pdf':
        FileHandler.delete_with_ending('../out_create/', '*.pdf')
    else:
        print(f'{type} not recognized')


def rename():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../out_create')
    for file_path in glob.glob(os.path.join(file_path, '*.txt')):
        if ' _ ' in file_path:
            os.rename(file_path, file_path.replace(" _ ", " & "))


if __name__ == "__main__":
    main()
    # rename()
    # delete_txt()
    # delete_pdf()
