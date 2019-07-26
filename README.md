# OCR Tester

## Description

This script creates PDFs containing Lorem Ipsum Text. It creates it for various fonts and fontsizes. 

After the PDFs are created, the RPA Tool runs over these and tries to OCR them. The outputs of that attempt are stored as txt files.

In the next step the scrips evaluates the recognized text against the encoded text. It calculates the
 [levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance?oldformat=true) of the words and summarizes 
 them in the `report.md`.

## Installation

You need to have python installed. To install python 3.7 just follow the steps of the [installer](https://www.python.org/downloads/).

Install the requirements by running `pip install --user -r requirements.txt` in the project directory.

## Usage

To create PDFs: `python -m ocr-test create --min 5 --max 25` where min describes the minimal font size and max 
the maximum font size.

To evaluate: `python -m ocr-test eval`. 
The Evaluation might, depending on the amount of files to evaluate, take some time.

## Add Fonts

Download the .ttf file of the font and add it to the `fonts` directory. It **must not**  have `_` (underscores) in the filename. Replace them with anything else if needed.

## Output

The Output file is a *MarkDown* file. To open it properly, if you have no MarkDown Viewer or Plugins for it,
 I recommend visiting [StackEdit](https://stackedit.io/app#), `Ctrl + A` the content in there and paste the content of report.md in there.