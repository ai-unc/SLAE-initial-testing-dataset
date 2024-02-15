# Obtain list of relations from Kumu or Vensim file

# Use the matcher to separate the list of relations, resulting in a series of python dictionaries each with a single paper and a list of related relations.

import json
with open("./test_inputs/output.json", "r") as f:
    matched_papers = json.loads(f)
print(matched_papers)
# Obtain settings by reading in the file

# For each dictionary run the "extract_relationships" function and settings

# Obtain a list of output jsons from the iterative running of extract_relationships

# Recombine the output jsons into the format required to output to Kumu

# Parse it into Kumu form and save the json in a file. 