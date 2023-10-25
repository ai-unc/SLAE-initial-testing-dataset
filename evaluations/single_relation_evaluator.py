"""
General purpose evaluator should take in a YAML file which specifies the parameters: type of model, evaluation dataset, type of scoring function, and supporting tools combination
Run the appropriate pipeline with these parameters.
Calculate the score.
Save results, score, predictions(inputs and outputs), other relevant information, in evaluation outputs.
"""
import sys
import pathlib
sys.path.append(str(pathlib.Path("../pipelines/")))
print(sys.path)
from single_variable_pipeline import extract_relationships
import json

# Read a YAML file
dataset_path = pathlib.Path("evaluations/evaluation_datasets/single_relation_dataset")

# Read evaluation dataset
dataset = json.load(dataset_path / "1.json")
print(dataset)

# Determine Settings

# extract_relationships()

# compare to obtain score