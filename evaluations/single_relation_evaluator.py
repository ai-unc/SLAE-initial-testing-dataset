"""
General purpose evaluator should take in a YAML file which specifies the parameters: type of model, evaluation dataset, type of scoring function, and supporting tools combination
Run the appropriate pipeline with these parameters.
Calculate the score.
Save results, score, predictions(inputs and outputs), other relevant information, in evaluation outputs.
"""
import pathlib
from pipelines.single_variable_pipeline import extract_relationships
import json
import os

mypath = os.path.abspath("")
print("___\n\n\n", mypath)

# Read a YAML file
dataset_path = pathlib.Path("evaluation_datasets/single_relation_dataset")

# Read evaluation dataset
with open(dataset_path / "1.json") as f:
    ground_truth = json.load(f)
    print("datatype of ground truth", type(ground_truth))

# Determine Settings
text = ground_truth["text"]
VariableOneName = ground_truth["VariableOneName"]
VariableTwoName = ground_truth["VariableTwoName"]
RelationshipClassification = ground_truth["RelationshipClassification"]
isCausal = ground_truth["isCausal"]

# extract_relationships()
# prediction = extract_relationships(text, VariableOneName, VariableTwoName).dict()
prediction = ground_truth.copy()
prediction["RelationshipClassification"] = "inverse"
print("datatype of prediction", type(prediction))
# compare to obtain score
def compare(prediction, ground_truth):
    score_dictionary = dict()
    if prediction["RelationshipClassification"] == ground_truth["RelationshipClassification"]:
        score_dictionary["RelationshipClassificationScore"] = 1
        print("RelationshipClassification Score ==> success")
    else:
        score_dictionary["RelationshipClassificationScore"] = 0
        print("RelationshipClassification Score ==> actual:", ground_truth["RelationshipClassification"], "; predicted:", prediction["RelationshipClassification"])
    
    if prediction["isCausal"] == ground_truth["isCausal"]:
        score_dictionary["isCausalScore"] = 1
        print("Causal Score ==> success")
    else:
        score_dictionary["isCausalScore"] = 0
        print("Causal Score ==> actual:", ground_truth["isCausal"], "; predicted:", prediction["isCausal"])

compare(prediction, ground_truth)