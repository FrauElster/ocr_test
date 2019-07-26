from abc import ABC
from dataclasses import dataclass
from typing import *

from mdutils import MdUtils

from . import utils
from .FileHandler import FileHandler


class Fail(ABC):
    title: str
    explanation: str

    def __init__(self, file_path: str):
        self.file_name: str = FileHandler.get_filename(file_path)
        self.font_name: str = self.file_name.split("_")[0]
        self.font_size: str = self.file_name.split("_")[-1]

    def __str__(self):
        raise Exception("To string not implemented")

    def to_md(self, mdFile: MdUtils) -> MdUtils:
        raise Exception("to_md not implemented")


class RecognitionFail(Fail):
    title = "Word Recognition Fails"

    def __init__(self, file_path: str, error_tuples: List[Tuple[str, str]]):
        super().__init__(file_path)
        self.error_words: List[WordFail] = list(
            map(lambda error_tuple: WordFail(error_tuple[0], error_tuple[1]), error_tuples))

    def __str__(self):
        return_string = f'{self.font_name} - {self.font_size}\n\n'
        for word_fail in self.error_words:
            return_string += f'{word_fail.__str__()}\n'

        return return_string

    def to_md(self, mdFile: MdUtils) -> MdUtils:
        mdFile.new_line(f'{self.font_name} - {self.font_size}:')
        md_text: List[str] = ['Word in PDF', 'Recognized Word', 'Levenshtein Distance']
        for word_fail in self.error_words:
            md_text.extend([word_fail.pdf_word, word_fail.ocr_word, str(word_fail.error_value)])
        mdFile.new_table(columns=3, rows=len(self.error_words) + 1, text=md_text, text_align='center')
        return mdFile


class LenFail(Fail):
    title = "Text Len Mismatch"
    explanation = "Font - "

    def __init__(self, file_path: str, ocr_len: int, pdf_len: int, total_levensthein: int):
        super().__init__(file_path)
        self.ocr_len: int = ocr_len
        self.pdf_len: int = pdf_len
        self.total_levensthein: int = total_levensthein

    def __str__(self):
        return f'{self.font_name} - {self.font_size}:\t{self.pdf_len}\t{self.ocr_len}\t{self.total_levensthein}'

    def to_md(self, mdFile: MdUtils) -> MdUtils:
        mdFile.new_line(str(self))
        return mdFile


class NoFail(Fail):
    title = "Passed Files"

    def __init__(self, file_path: str):
        super().__init__(file_path)

    def __str__(self):
        return f'{self.font_name} - {self.font_size}'

    def to_md(self, mdFile: MdUtils) -> MdUtils:
        mdFile.new_line(str(self))
        return mdFile


class WordFail:
    def __init__(self, pdf_word: str, ocr_word: str):
        self.pdf_word: str = pdf_word
        self.ocr_word: str = ocr_word
        self.error_value: int = utils.levenstein(pdf_word, ocr_word)

    def __str__(self):
        return f'{self.pdf_word}\t{self.ocr_word}\t{self.error_value}'
