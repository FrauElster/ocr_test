import os
import glob
from typing import *
from tika import parser
import json

from src.Fail import Fail


def main(path: str):
    passed_files: List[str] = []
    fails: List[Fail] = []

    should_read = get_lorem()
    for filename in glob.glob(os.path.join(path, '*.pdf')):
        file_words = get_pdf_words(filename)
        if len(file_words) != len(should_read):
            fails.append(Fail(filename, is_len_error=True))
            continue

        error_tuples: List[Tuple[str, str]] = []
        for word_ind in range(len(file_words)):
            read_word = file_words[word_ind]
            should_word = should_read[word_ind]
            if read_word != should_word:
                error_tuples.append((should_word, read_word))

        if len(error_tuples) == 0:
            passed_files.append(filename)
            print(f'File {filename} passed')
        else:
            fails.append(Fail(filename, error_tuples=error_tuples))

    report(fails)
    print(f'Passed files: {passed_files}')
    log_fails(fails)


def get_lorem():
    lorem = open('../lorem.txt').read()
    lorem_lines = lorem.split('\n')
    lorem_words: List[str] = []
    for line in lorem_lines:
        lorem_words.extend(line.split(" "))
    return lorem_words


def get_pdf_words(filename: str):
    words: List[str] = []
    raw = parser.from_file(filename)
    pdf_content = raw['content']
    pdf_lines = pdf_content.split("\n")
    for line in pdf_lines:
        words.extend(line.split(" "))
    return words


def report(fails: List[Fail]):
    font_dict_len_err = {}
    font_dict_no_len_err = {}
    for fail in fails:
        if fail.is_len_error:
            if fail.font_name not in font_dict_len_err.keys():
                font_dict_len_err[fail.font_name] = []

            font_dict_len_err[fail.font_name].append(fail.font_size)
        else:
            total_error_count: int = sum(list(map(lambda error_word: error_word.error_value, fail.error_words)))
            if fail.font_name not in font_dict_no_len_err.keys():
                font_dict_no_len_err[fail.font_name] = []

            font_dict_no_len_err[fail.font_name].append([fail.font_size, total_error_count])

    out_text = f'{get_len_err_text(font_dict_len_err)}\n\n{get_len_no_err_text(font_dict_no_len_err)}'

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", 'report.txt')
    file = open(file_path, "w")
    file.write(out_text)


def get_len_no_err_text(font_dict):
    out_text = "Word fails:\n\n"
    for font in font_dict.keys():
        out_text += f'{font}\n'
        for size_ind in range(len(font_dict[font])):
            size = font_dict[font][size_ind][0]
            error_sum = font_dict[font][size_ind][1]
            out_text += f'\tSize: {size}\tError Sum: {error_sum}\n'
    return out_text


def get_len_err_text(font_dict):
    out_text = 'Word count mismatch:\n\n'
    for font in font_dict.keys():
        out_text += f'{font}\n\tFont sizes: '
        for size in font_dict[font]:
            out_text += f'{size}, '
        out_text += "\n"
    return out_text


def log_fails(fails: List[Fail]):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", 'out.json')
    fails_serializable = serialize_data(fails)
    file = open(file_path, 'w')
    file.write(json.dumps(fails_serializable))


def serialize_data(fails: List[Fail]):
    fails_copy = fails.copy()
    for fail in fails_copy:
        fail.error_words = list(map(lambda error_word: error_word.__dict__, fail.error_words))
    return list(map(lambda fail: fail.__dict__, fails_copy))


def get_words(filename):
    file_content = open(filename).read()
    file_lines = file_content.split("\n")
    file_words = []
    for line in file_lines:
        file_words.extend(line.split(" "))

    pdf_filename = ""
    pdf_filename_list = filename.split("_")
    pdf_filename_list = pdf_filename_list[:-1]
    for sub_filename in pdf_filename_list:
        pdf_filename += sub_filename + "_"
    pdf_filename = pdf_filename[:-1]
    pdf_filename += ".pdf"

    raw = parser.from_file(pdf_filename)
    pdf_content = raw['content']
    pdf_lines = pdf_content.split("\n")

    pdf_words = []
    pdf_words_tmp = []
    for line in pdf_lines:
        pdf_words_tmp.extend(line.split(" "))
    for word in pdf_words_tmp:
        if len(word) != 0:
            pdf_words.append(word)

    return file_words, pdf_words


if __name__ == "__main__":
    # test()
    main('../out_create/')
