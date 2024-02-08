"""Extracts tuples/lists of variable names without duplicates from input files"""
import json 
import pathlib
import os


def extract_all_unique_pairs(file_path):
    #Load the json file
    # directory = os.getcwd()
    # inputs_path = directory + "/inputs"
    # file_name = "test_paper.json"
    # file_path = os.path.join(inputs_path, file_name)

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
    return variable_pairs

def extract_all_ordered_pairs(data):
    #Extract the relationships
    relationships = data.get("Relations", [])
    #Store unique ordered pairs of variables
    variable_pairs = []
    # Iterate through each relationship and extract variables
    for relationship in relationships:
        variable_one = relationship.get("VariableOneName", "")
        variable_two = relationship.get("VariableTwoName", "")
        variable_pairs.append(variable_one + " -> " + variable_two)
    # Print the resulting list of variable lists
    relations_text = "\n".join(variable_pairs)
    return relations_text

if __name__ == "__main__":
    ans = extract_all_ordered_pairs("../evaluation_datasets/multi_relation_dataset/test_paper.json")
    print(ans)