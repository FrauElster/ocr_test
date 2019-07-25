import glob
import os

import click

from src import create_pdf, evaluate


@click.group()
def main():
    pass


@click.command()
@click.option('--max', 'min_font_size', type=int, required=True, help="Max font size")
@click.option('--min', 'max_font_size', type=int, required=True, help="Min font size")
def create(min_font_size, max_font_size):
    create_pdf.main(min_font_size, max_font_size)


@click.command()
@click.option('--path', type=str, default='../out_create/', help="Path to PDFs")
def eval(path: str):
    evaluate.main(path)


def delete_txt():
    for filename in glob.glob(os.path.join('../out_create/', '*.txt')):
        os.remove(filename)


if __name__ == "__main__":
    #main()
    delete_txt()