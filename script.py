import sys, os, re, json

fileFlag = sys.argv[1]
doiFlag = sys.argv[2]
titleFlag = sys.argv[3]

if not fileFlag.startswith("-file=") or len(fileFlag) < 7:
    sys.exit("Invalid file flag")
if not doiFlag.startswith("-doi=") or len(doiFlag) < 6:
    sys.exit("Invalid doi flag")
if not titleFlag.startswith("-title=") or len(titleFlag) < 8:
    sys.exit("Invalid title flag")


doi = doiFlag.split("=")[1]
fileNameSafeDoi = re.sub("[^a-zA-Z0-9\n\.]", "_", doi)

title = titleFlag.split("=")[1]
fileNameSafeTitle = re.sub("[^a-zA-Z0-9\n\.]", "_", title)
shortTitle = ""
titleChunks = fileNameSafeTitle.split("_")
for chunk in titleChunks[:5]:
    if len(shortTitle + chunk) < 45:
        shortTitle += chunk
    else:
        break

filePath = fileFlag.split("=")[1]
fileExt = "." + filePath.split(".").pop()
filePath = "papers/" + filePath
fileName = shortTitle + "_" + fileNameSafeDoi
newFilePath = "papers/" + fileName + fileExt
os.rename(filePath, newFilePath)

print(title)

inputData = {
    "PaperDOI": doi,
    "PaperTitle": title,
    "PaperContents": "",
    "Variables": [
        {
            "VariableOneName": "",
            "VariableTwoName": "",
            "RelationshipClassification": "",
            "SupportingText": "",
        }
    ],
}
print(inputData["PaperTitle"])
serializedInputData = json.dumps(inputData, indent=4)
with open("inputs/" + fileName + ".json", "w") as outfile:
    outfile.write(serializedInputData)
