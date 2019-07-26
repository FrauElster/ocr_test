import glob
import os
import click

from . import create_pdf, evaluate


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


def delete_txt():
    for filename in glob.glob(os.path.join('../out_create/', '*.txt')):
        os.remove(filename)


def rename():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../out_create')
    for file_path in glob.glob(os.path.join(file_path, '*.txt')):
        if ' _ ' in file_path:
            os.rename(file_path, file_path.replace(" _ ", " & "))


if __name__ == "__main__":
    main()
    # rename()
    # delete_txt()