import glob
import os
import typing

from tika import parser


class FileHandler:
    @staticmethod
    def get_path(file_path) -> str:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_path)

    @staticmethod
    def load_file(file_path) -> typing.Optional[str]:
        if os.path.isfile(file_path):
            return open(file_path).read()
        else:
            print(f'{file_path} not found')

    @staticmethod
    def load_pdf(file_path: str):
        raw = parser.from_file(file_path)
        return raw['content']

    @staticmethod
    def txt_to_pdf_filepath(txt_filename: str) -> str:
        dir_path = txt_filename.split("/")
        pdf_filename = dir_path.pop(-1)
        dir_path = "/".join(dir_path)
        pdf_filename = dir_path + '/' + pdf_filename.split(".")[0] + '.pdf'
        return pdf_filename

    @staticmethod
    def get_filename(file_name) -> str:
        file_name = file_name.split('/')[-1]
        return file_name.split(".")[0]

    @staticmethod
    def append_to_file_if_exists(file_path: str, content: str):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_path)
        if os.path.isfile(file_path):
            file = open(file_path, 'a')
        else:
            file = open(file_path, 'w')
        file.write(content)

    @staticmethod
    def write_file(file_path: str, content: str):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_path)
        file = open(file_path, 'w')
        if file.writable():
            file.write(content)
            return True
        return False

    @staticmethod
    def list_words(content: str) -> typing.List[str]:
        words: typing.List[str] = []
        for line in content.split("\n"):
            words.extend(list(filter(lambda word: word != "", line.split(" "))))
        return words

    @staticmethod
    def delete_with_ending(dir_path: str, ending: str) -> bool:
        dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), dir_path)
        if os.path.isdir(dir_path):
            for file_path in glob.glob(os.path.join(dir_path, '*.*')):
                if file_path.split(".")[-1] == ending:
                    os.remove(file_path)
            return True
        else:
            print(f'{dir_path} is not a directory')
            return False
