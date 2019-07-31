import glob
import os
import time
from typing import *

from mdutils import MdUtils

from . import utils
from .Fail import Fail, LenFail, RecognitionFail, NoFail
from .FileHandler import FileHandler


def main(path: str):
    file_path = FileHandler.get_path(path)
    fail_dict = analyse(file_path)
    report(fail_dict)


def analyse(filepath: str) -> Dict[str, List[Fail]]:
    print("Starting to analyse")
    start_time = time.time()
    fail_dict: Dict[Fail, List[Fail]] = {}
    for fail_class in Fail.__subclasses__():
        fail_dict[fail_class] = []

    txt_files: List[str] = glob.glob(os.path.join(filepath, '*.txt'))
    if not txt_files:
        print(f'No txt files found to evaluate. Make sure the OCR recognized txt files are in {filepath}')
        exit(1)

    for file_path in txt_files:

        ocr_content: str = FileHandler.load_file(file_path)
        pdf_filepath: str = FileHandler.txt_to_pdf_filepath(file_path)
        pdf_content: str = FileHandler.load_pdf(pdf_filepath)

        ocr_words: List[str] = FileHandler.list_words(ocr_content)
        pdf_words: List[str] = FileHandler.list_words(pdf_content)

        total_levenstein: int = utils.levenstein(ocr_content, pdf_content)

        if len(ocr_words) != len(pdf_words):
            fail_dict[LenFail].append(LenFail(file_path, len(ocr_words), len(pdf_words), total_levenstein))
            continue

        error_tuples: List[Tuple[str, str]] = []
        for word_ind in range(len(ocr_words)):
            ocr_word: str = ocr_words[word_ind]
            pdf_word: str = pdf_words[word_ind]
            if not ocr_word == pdf_word:
                error_tuples.append((pdf_word, ocr_word))

        if error_tuples:
            fail_dict[RecognitionFail].append(RecognitionFail(file_path, error_tuples, total_levenstein))
            continue

        fail_dict[NoFail].append(NoFail(file_path))

    for fail_typ in fail_dict.keys():
        fail_dict[fail_typ].sort(key=lambda fail: fail.total_levenshtein)

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
        mdFile.new_header(level=3, title="Fails", add_table_of_contents='n')
        mdFile.new_line()

        if fail_typ == LenFail:
            md_text: List[str] = ['Font name - size', 'Words in PDF', 'Recognized words',
                                  'Levenshtein distance of total text']
            for len_fail in fails[fail_typ]:
                md_text.extend(
                    [f'{len_fail.font_name} - {len_fail.font_size}', str(len_fail.pdf_len), str(len_fail.ocr_len),
                     str(len_fail.total_levenshtein)])

            mdFile.new_table(columns=4, rows=int(len(md_text) / 4), text=md_text, text_align='center')
        else:
            for fail in fails[fail_typ]:
                mdFile = fail.to_md(mdFile)

    mdFile.create_md_file()
    print(f'Finished reporting after {time.time() - start_time} sec')
