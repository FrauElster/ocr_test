# OCR Tester

## Description

This script creates PDFs containing Lorem Ipsum Text. It creates it for various fonts and fontsizes. 

After the PDFs are created, the RPA Tool runs over these and tries to OCR them. The outputs of that attempt are stored as txt files.

In the next step the scrips evaluates the recognized text with the Lorem Ipsum. It calculates the [levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance?oldformat=true) of the words and summarizes them in the `report.txt`. Also for further work the errors will be stored in the `out.json`.

## Installation

You need to have python installed. To install python 3.7 just follow the steps of the [installer](https://www.python.org/downloads/).

Install the requirements by running `pip install --user -r requirements.txt` in the project directory.

## Usage

To create PDFs: `python -m ocr-tester create --min 5 --max 25` where min describes the minimal font size and max the maximum font size.

To evaluate: `python -m ocr-tester eval`

## Add Fonts

Download the .ttf file of the font and add it to the `fonts` directory. It **must not**  have `_` (underscores) in the filename. Replace them with anything else if needed.