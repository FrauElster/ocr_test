import os
import glob
from tika import parser

PATH = r'C:\Users\mori\Documents\Servicetrace\pdfs'

def test():
    for filename in glob.glob(os.path.join(PATH, '*.txt')):
        read_words, lorem_words = get_words(filename)
        print("--------------------------READ--------------------------------")
        print(read_words)
        print("-------------------------SHOULD-------------------------------")
        print(lorem_words)
        print("--------------------------------------------------------------")
        break


def main():
    passed_files = []
    fail_dict = {}
    for filename in glob.glob(os.path.join(PATH, '*.txt')):
        file_words, lorem_words = get_words(filename)
        fail_dict[filename] = []
        print(f'DEBUG filename: {filename}')
    
        for word_ind in range(len(file_words)):
            read_word = file_words[word_ind]
            should_word = lorem_words[word_ind]  
            if  read_word != should_word:
                fail_dict[filename].append((should_word, read_word))

        if len(fail_dict[filename]) == 0:
            passed_files.append(filename)
            print(f'File {filename} passed')

    print_fails(fail_dict)
    print(f'Passed files: {passed_files}')


def print_fails(fail_dict: dict):
    print("--------------------------FAILS------------------------")
    for filename in fail_dict.keys():
        for fail in fail_dict[filename]:
            print(f'{filename}\tShould: {fail[0]}\tIs:{fail[1]}')

    print("\n")



def get_lorem():
    'Lorem not available'
    if os.path.exists('lorem.txt'):
        lorem = open('lorem.txt').read()
    else:
        print("lorem.txt not found!\nAbort")
        exit()
    lorem_line = lorem.split(" ")
    lorem_list = []
    for line in lorem_line:
        lorem_list.extend(line.split(" "))
    return lorem_list


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
    #test()
    main()