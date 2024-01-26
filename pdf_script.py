import sys
import os
import re
import json
from PyPDF2 import PdfReader
from typing import List, Tuple
import fitz

def extract_sticky_notes(pdf_path):
    sticky_notes = []
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            if '/Annots' in page:
                annotations = page['/Annots']
                for annot in annotations:
                    annotation_object = annot.get_object()
                    if '/Contents' in annotation_object:
                        contents = annotation_object['/Contents']
                        variable_one_name = re.search(r'variable 1: (.+?)\n', contents, re.IGNORECASE)
                        variable_two_name = re.search(r'variable 2: (.+?)\n', contents, re.IGNORECASE)
                        relationship_classification = re.search(r'relationship: (.+?)(?:\n|$)', contents, re.IGNORECASE)
                        is_causal = re.search(r'is causal: (.+?)\n', contents, re.IGNORECASE)
                        attributes = re.search(r'attributes: (.+?)(?:\n|$)', contents, re.IGNORECASE)
                        supporting_text = re.search(r'text: (.+?)(?:\n|$)', contents, re.IGNORECASE)
                        sticky_notes.append({
                            'VariableOneName': variable_one_name.group(1) if variable_one_name else "",
                            'VariableTwoName': variable_two_name.group(1) if variable_two_name else "",
                            'RelationshipClassification': relationship_classification.group(1) if relationship_classification else "",
                            'IsCausal': is_causal.group(1) if is_causal else "",
                            'Attributes': attributes.group(1) if attributes else "",
                            'SupportingText': supporting_text,
                        })
    return sticky_notes


def extract_pdf_text(pdf_path):
    text_contents = []
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text_contents.append(page.extract_text())
    return text_contents

def sanitize_text(text):
    return re.sub("[^a-zA-Z0-9\n ]", "_", text)

def main(pdf_path, doi, title):
    sticky_notes = extract_sticky_notes(pdf_path)
    text_contents = extract_pdf_text(pdf_path)
    file_contents = "".join(text_contents)
    file_contents = sanitize_text(file_contents)
    input_data = {
        "PaperDOI": doi,
        "PaperTitle": title,
        "PaperContents": file_contents,
        "Variables": sticky_notes,
    }
    serialized_input_data = json.dumps(input_data, indent=4)
    file_name = f"{title}_{re.sub('[^a-zA-Z0-9]', '_', doi)}.json"
    with open(f"inputs/{file_name}", "w") as outfile:
        outfile.write(serialized_input_data)


def parse_arguments(args):
    arg_dict = {}
    for arg in args[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            arg_dict[key] = value
    return arg_dict

if __name__ == "__main__":
    # Parse command line arguments
    arg_dict = parse_arguments(sys.argv)

    # Check for required flags
    if not all(flag in arg_dict for flag in ['-pdf', '-doi', '-title']):
        print("Invalid or missing arguments")
        sys.exit("Usage: python pdf_script.py -pdf=PDF_PATH -doi=DOI -title=TITLE")

    # Extract values from the dictionary
    pdf_path = arg_dict['-pdf']
    doi = arg_dict['-doi']
    title = arg_dict['-title']

    pdf_flag, doi_flag, title_flag = sys.argv[1:4]
    # Validate PDF flag
    if not pdf_flag.startswith("-pdf=") or not pdf_flag.endswith('.pdf'):
        sys.exit("Invalid PDF flag")

    # Validate doi flag
    if not doi_flag.startswith("-doi=") or len(doi_flag) < 6:
        sys.exit("Invalid doi flag")

    # Validate title flag
    if not title_flag.startswith("-title=") or len(title_flag) < 8:
        sys.exit("Invalid title flag")

    # Extract doi and title
    doi = doi_flag.split("=")[1]
    title = title_flag.split("=")[1]

    # Extract PDF path
    pdf_path = pdf_flag.split("=")[1]

    # Perform main processing
    main(pdf_path, doi, title)


# $ git commit -m "PDF Reader script" pdf_script.py ronald.pdf
# $ git push
    
#git checkout -b feat/pdf-reader
# git checkout feat/pdf-reader
# git commit -m "PDF Reader script" pdf_script.py ronald.pdf
# git push -u origin name-of-branch



