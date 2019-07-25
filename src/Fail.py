from typing import *


class Fail:
    def __init__(self, file_name: str, is_len_error=False, error_tuples: List[Tuple[str, str]] = []):
        self.file_name: str = Fail._get_filename(file_name)
        self.font_name: str = self.file_name.split("_")[0]
        self.font_size: str = self.file_name.split("_")[-1]
        self.is_len_error: bool = is_len_error
        self.error_words: List[Word_Fail] = list(
            map(lambda error_tuple: Word_Fail(error_tuple[0], error_tuple[1]), error_tuples))

    @staticmethod
    def _get_filename(file_name) -> str:
        file_name = file_name.split('\\')[1]
        return file_name.split(".")[0]


class Word_Fail:
    def __init__(self, should_word: str, is_word: str):
        self.should_word: str = should_word
        self.is_word: str = is_word
        self.error_value: int = Word_Fail._levenstein(should_word, is_word)

    @staticmethod
    def _levenstein(s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return Word_Fail._levenstein(s2, s1)

        # len(s1) >= len(s2)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[
                                 j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
                deletions = current_row[j] + 1  # than s2
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]
