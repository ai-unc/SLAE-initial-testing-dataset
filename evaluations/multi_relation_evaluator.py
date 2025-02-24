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
    if prediction["RelationshipClassification"].lower() == ground_truth["RelationshipClassification"].lower():
        score_dictionary["RelationshipClassificationScore"] = 1
        print("RelationshipClassification Score ==> success;", ground_truth["RelationshipClassification"])
    else:
        score_dictionary["RelationshipClassificationScore"] = 0
        print("RelationshipClassification Score ==> actual:", ground_truth["RelationshipClassification"], "; predicted:", prediction["RelationshipClassification"])
    
    if prediction["isCausal"].lower() == ground_truth["isCausal"].lower():
        score_dictionary["isCausalScore"] = 1
        print("Causal Score ==> success; ", ground_truth["isCausal"])
    else:
        score_dictionary["isCausalScore"] = 0
        print("Causal Score ==> actual:", ground_truth["isCausal"], "; predicted:", prediction["isCausal"])
    return score_dictionary

# Read a YAML file
dataset_path = pathlib.Path("evaluation_datasets/multi_relation_dataset")

# Read evaluation dataset
with open(dataset_path / "test_paper.json") as f:
    ground_truth = json.load(f)
    print("datatype of ground truth", type(ground_truth))    

# Determine Settings
text = ground_truth["text"]
# extract_relationships based on settings (which is text and nothing else)
if True:
    predictions = extract_relationships(text).dict()
else:
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

with open("evaluation_outputs/multi_relation_results/results.txt", "w") as f:
    f.write("Predictions\n")
    f.write(json.dumps(predictions, indent=2))
    f.write("Ground Truth\n")
    f.write(json.dumps(ground_truth, indent=2))
    f.write("Results\n")
    f.write(json.dumps(aggregate_results, indent=2))