"""
General purpose evaluator should take in a YAML file which specifies the parameters: type of model, evaluation dataset, type of scoring function, and supporting tools combination
Run the appropriate pipeline with these parameters.
Calculate the score.
Save results, score, predictions(inputs and outputs), other relevant information, in evaluation outputs.
"""
import pathlib
from pipelines.multi_paper_pipeline import extract_relationships
import json
import os
from copy import deepcopy

mypath = os.path.abspath("")
print("___\n\n\n", mypath)

def compare(prediction, ground_truth):
    score_dictionary = dict()
    print(prediction["RelationshipClassification"], ground_truth["RelationshipClassification"])
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
    return score_dictionary
# Read a YAML file
dataset_path = pathlib.Path("evaluation_datasets/multi_relation_dataset")

# Read evaluation dataset
with open(dataset_path / "partner_violence_and_alcohol_exposed_prengancy_10.1111_acer.13968.json") as f:
    ground_truth = json.load(f)
    print("datatype of ground truth", type(ground_truth))    

# Determine Settings
text = ground_truth["text"]
# extract_relationships based on settings (which is text and nothing else)
# prediction = extract_relationships(text, VariableOneName, VariableTwoName).dict()
predictions = deepcopy(ground_truth)
predictions["Relations"][0]["RelationshipClassification"] = "inverse"
print("datatype of prediction", type(predictions))
# compare to obtain score

if len(predictions["Relations"]) > len(ground_truth["Relations"]):
    index_max = len(ground_truth["Relations"])
else: index_max = len(predictions["Relations"])

results: list(dict()) = list()
for relation_index in range(index_max):
    relation = ground_truth["Relations"][relation_index]
    prediction = predictions["Relations"][relation_index]
    results.append(compare(prediction, relation))

aggregate_results = dict()
aggregate_results["RelationshipClassificationScore"] = 0
aggregate_results["CausalIdentificationScore"] = 0
for x, result in enumerate(results):
    aggregate_results["RelationshipClassificationScore"] += result["RelationshipClassificationScore"]
    aggregate_results["CausalIdentificationScore"] += result["isCausalScore"]
aggregate_results["RelationshipClassificationScore"] /= (x + 1)
aggregate_results["CausalIdentificationScore"] /= (x + 1)
print(aggregate_results)
