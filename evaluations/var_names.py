"""Extracts tuples/lists of variable names without duplicates from input files"""
import json 
import pathlib
import os

#Load the json file
directory = os.getcwd()
inputs_path = directory + "/SLAE-initial-testing-dataset" + "/inputs"
file_name = "duplicate_test.json"
file_path = os.path.join(inputs_path, file_name)

with open(file_path, 'r', encoding='utf-8') as file:
    paper = json.load(file)
#Extract the relationships
relationships = paper.get("Variables", [])
#Store unique ordered pairs of variables
variable_pairs = []
# Create a set to check for uniqueness
seen_pairs = set()
# Iterate through each relationship and extract variables
for relationship in relationships:
    variable_one = relationship.get("VariableOneName", "")
    variable_two = relationship.get("VariableTwoName", "")

    # Check for uniqueness based on both orders of the pair
    pair_1 = (variable_one, variable_two)
    pair_2 = (variable_two, variable_one)
    if pair_1 not in seen_pairs and pair_2 not in seen_pairs:
        variable_pairs.append([variable_one, variable_two])
        seen_pairs.add(pair_1)
# Print the resulting list of variable lists
print(variable_pairs)