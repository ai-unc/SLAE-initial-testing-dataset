# Import necessary modules
import os, re, json

# Check for help flag
# if sys.argv[1] == "-h" or sys.argv[1] == "--help":
#     print("Usage: python script.py -file=FILE -doi=DOI -title=TITLE")
#     print("FILE: The name of the file containing the paper.")
#     print("DOI: The DOI of the paper.")
#     print("TITLE: The title of the paper.")
#     sys.exit()

# # Check for correct number of arguments
# if len(sys.argv) < 4 or len(sys.argv) > 4:
#     print("Invalid number of arguments")
#     sys.exit("Type 'python script.py -h' for help")

# # Extract command line arguments
# fileFlag = sys.argv[1]
# doiFlag = sys.argv[2]
# titleFlag = sys.argv[3]

# # Validate file flag
# if not fileFlag.startswith("-file=") or len(fileFlag) < 7 or not fileFlag.endswith('.txt'):
#     sys.exit("Invalid file flag")

# # Validate doi flag
# if not doiFlag.startswith("-doi=") or len(doiFlag) < 6:
#     sys.exit("Invalid doi flag")

# # Validate title flag
# if not titleFlag.startswith("-title=") or len(titleFlag) < 8:
#     sys.exit("Invalid title flag")

# Extract doi, sanitize and create safe file name
def paper_to_input(filePath, doi, title):
    #doi = doiFlag.split("=")[1]
    fileNameSafeDoi = re.sub("[^a-zA-Z0-9\n\.]", "_", doi)

    # Extract title, sanitize and create safe file name
    #title = titleFlag.split("=")[1]
    fileNameSafeTitle = re.sub("[^a-zA-Z0-9\n\.]", "_", title)
    shortTitle = ""
    titleChunks = fileNameSafeTitle.split("_")

    # Create a short title for the file name
    for chunk in titleChunks[:5]:
        if len(shortTitle + chunk) < 45:
            shortTitle += chunk
        else:
            break

    # Create file paths and rename/move the file
    #filePath = fileFlag.split("=")[1]
    fileExt = "." + filePath.split(".").pop()
    filePath = "papers/" + filePath
    fileName = shortTitle + "_" + fileNameSafeDoi
    newFilePath = "papers/" + fileName + fileExt

    try:
        os.rename(filePath, newFilePath)
    except IOError:
        f = open(newFilePath, "x")
        f.close()

    fileContents = ""

    # Read the file contents and sanitize each line
    with open(newFilePath, "r", encoding="utf8") as f:
        lines = f.readlines()

    # Write the sanitized lines back to the file
    with open(newFilePath, "w", encoding="utf8") as f:
        for line in lines:
            line = re.sub("[^a-zA-Z0-9\n ]", "_", line)
            fileContents += line
            f.write(line)

    # Create input data dictionary
    inputData = {
        "PaperDOI": doi,
        "PaperTitle": title,
        "PaperContents": fileContents,
        "Relations": [
            {
                "VariableOneName": "",
                "VariableTwoName": "",
                "RelationshipClassification": "",
                "IsCausal": "",
                "SupportingText": "",
            }
        ],
    }

    # Serialize input data to JSON format
    serializedInputData = json.dumps(inputData, indent=4)

    # Write the serialized input data to a JSON file
    with open("inputs/" + fileName[:45] + ".json", "w") as outfile: # limit file name just in case
        outfile.write(serializedInputData)

# if __name__ == "__main__":
#     cwd = "./papers" # this is currently full of pdfs and not txts
#     for file in os.listdir(cwd):
#         if file.endswith(".txt"):
#             main(file, "123434", "a very long and interesting title")