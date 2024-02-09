import os
import json


papers = []

cwd = "../evaluations/auto_generated_inputs"
for file in os.listdir(cwd):
    input_path = os.path.join(cwd, file)
    with open(input_path, "r") as f:
        json.load(f)
        papers.append(f)
        print(input_path)
