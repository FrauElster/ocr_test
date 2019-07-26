import glob
import os
import time
from typing import *

from mdutils import MdUtils

from . import utils
from .Fail import Fail, LenFail, RecognitionFail, NoFail
from .FileHandler import FileHandler


def main(path: str):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    fail_dict = analyse(file_path)
    report(fail_dict)


def analyse(filepath: str) -> Dict[str, List[Fail]]:
    print("Starting to analyse")
    start_time = time.time()
    fail_dict: Dict[str, List[Fail]] = {}
    for fail_class in Fail.__subclasses__():
        fail_dict[fail_class] = []

    for file_path in glob.glob(os.path.join(filepath, '*.txt')):

        ocr_content: str = FileHandler.load_file(file_path)
        pdf_filepath: str = FileHandler.txt_to_pdf_filepath(file_path)
        pdf_content: str = FileHandler.load_pdf(pdf_filepath)

        ocr_words: List[str] = FileHandler.list_words(ocr_content)
        pdf_words: List[str] = FileHandler.list_words(pdf_content)

        if len(ocr_words) != len(pdf_words):
            total_levenstein: int = utils.levenstein(ocr_content, pdf_content)
            fail_dict[LenFail].append(LenFail(file_path, len(ocr_words), len(pdf_words), total_levenstein))
            continue

        error_tuples: List[Tuple[str, str]] = []
        for word_ind in range(len(ocr_words)):
            ocr_word: str = ocr_words[word_ind]
            pdf_word: str = pdf_words[word_ind]
            if not ocr_word == pdf_word:
                error_tuples.append((pdf_word, ocr_word))

        if error_tuples:
            fail_dict[RecognitionFail].append(RecognitionFail(file_path, error_tuples))
            continue

        fail_dict[NoFail].append(NoFail(file_path))

    print(f'Finished analysing after {time.time() - start_time} sec')
    return fail_dict


def report(fails: Dict[str, List[Fail]]):
    print('Start writing report')
    start_time = time.time()
    mdFile = MdUtils(file_name='report', title='OCR Recognition Report')

    for fail_typ in fails.keys():
        mdFile.new_header(level=2, title=fail_typ.title, add_table_of_contents='n')
        mdFile.new_header(level=3, title="Explanation", add_table_of_contents='n')
        mdFile.new_paragraph(fail_typ.explanation)
        mdFile.new_line(f'There were in total {len(fails[fail_typ])} of {fail_typ.title}')
        for fail in fails[fail_typ]:
            mdFile = fail.to_md(mdFile)

    mdFile.create_md_file()
    print(f'Finished reporting after {time.time() - start_time} sec')


if __name__ == "__main__":
    main(file_path)
