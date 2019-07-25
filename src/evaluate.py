import os
import glob
from typing import *
import json
from tika import parser

from src.Fail import Fail, Word_Fail


def get_pdf_content(pdf_filename):
    raw = parser.from_file(pdf_filename)
    return raw['content']


def test(path: str):
    for filepath in glob.glob(os.path.join(path, '*.txt')):
        txt_content = open(filepath).read()

        pdf_filename = txt_to_pdf_filename(filepath)
        pdf_content = get_pdf_content(pdf_filename)

        levenstein: int = Word_Fail._levenstein(pdf_content, txt_content)
        filename = filepath.split("/")[-1]
        filename = filename.split(".")[0]
        test_report(filename, levenstein)


def txt_to_pdf_filename(txt_filenmae: str):
    dir_path = txt_filenmae.split("/")
    pdf_filename = dir_path.pop(-1)
    dir_path = "/".join(dir_path)
    pdf_filename = dir_path + '/' + pdf_filename.split(".")[0] + '.pdf'
    return pdf_filename


def test_report(filename: str, levenstein: int):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", 'test_report.txt')
    if os.path.exists(file_path):
        file = open(file_path, 'a')
    else:
        file = open(file_path, 'w')
    file.write(f'{filename}:\t{levenstein}\n')


def main(path: str):
    passed_files: List[str] = []
    fails: List[Fail] = []

    for filename in glob.glob(os.path.join(path, '*.txt')):
        file_words = get_pdf_words(filename)
        pdf_filename = txt_to_pdf_filename(filename)
        should_read = get_lorem(pdf_filename)
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
    log_fails(fails)


def get_lorem(pdf_filename):
    raw = parser.from_file(pdf_filename)
    lorem =  raw['content']
    lorem_lines = lorem.split('\n')
    lorem_words: List[str] = []
    for line in lorem_lines:
        lorem_words.extend(line.split(" "))
    return lorem_words


def get_pdf_words(filename: str):
    words: List[str] = []
    pdf_content = open(filename).read()
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


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", 'out_create/')
    test(file_path)
    main(file_path)
