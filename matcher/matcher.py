import os
import json
from pprint import pprint

# def passage_rank(relation, papers, threshold=.5):
#     paper_texts = [i["PaperContents"] for i in papers]
#     relevant_papers = [{"PaperDOI": "10.1002/cpp.1896"}, {"PaperDOI": "10.3389/fpsyg.2022.1016879"}]
#     score = []
#     for i in score:
#         if i > threshold:
#             relevant_papers.append(paper_texts[i])
#     return relevant_papers

from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

# Initialize the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def compute_similarity(embedding1, embedding2):
    # Cosine similarity
    return np.dot(embedding1, embedding2.T) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

def passage_rank(relation, papers, threshold=0.25):
    # Tokenize and encode the relation
    inputs = tokenizer(relation, return_tensors="pt", padding=True, truncation=True, max_length=512)
    relation_embedding = model(**inputs).last_hidden_state.mean(dim=1).detach().numpy()
    
    relevant_papers = []
    for paper in papers:
        # Tokenize and encode each paper
        paper_inputs = tokenizer(paper["PaperContents"], return_tensors="pt", padding=True, truncation=True, max_length=512)
        # paper inputs are a dictionary consisting of the embeddings, type, and attention mask.
        paper_embedding = model(**paper_inputs).last_hidden_state.mean(dim=1).detach().numpy()
        
        # Compute similarity
        similarity = compute_similarity(relation_embedding, paper_embedding)
        print(paper["PaperTitle"][:50], relation, similarity)
        if similarity > threshold:
            relevant_papers.append(paper)
    return relevant_papers


papers = []

PAPERS_DIRECTORY = "../evaluations/auto_generated_inputs"
INPUT_RELATIONS_DIRECTORY = "../evaluations/test_inputs/test_input.json"
for file in os.listdir(PAPERS_DIRECTORY):
    input_path = os.path.join(PAPERS_DIRECTORY, file)
    with open(input_path, "r") as f:
        data = json.load(f)
        papers.append(data)
        # print(input_path)


input_path = INPUT_RELATIONS_DIRECTORY
with open(input_path, "r") as f:
    data = json.load(f)
relationships = data["Relations"]

variable_pairs = []
# Iterate through each relationship and extract variables
for relationship in relationships:
    variable_one = relationship.get("VariableOneName", "")
    variable_two = relationship.get("VariableTwoName", "")
    variable_pairs.append(variable_one + " -> " + variable_two)

print(variable_pairs)

relations_and_ranked_papers: dict = dict()
for i in range(len(variable_pairs)):
    relation = variable_pairs[i]
    relevant_papers = passage_rank(relation, papers) # relevant papers is a list of relevant paper dictionaries with relevant metadata
    relations_and_ranked_papers[i] = {j["PaperDOI"] for j in relevant_papers}

print(relations_and_ranked_papers)

# Goal: something in the form of list of paper objects with relations
for i in range(len(papers)):   
    papers[i]["Relations"] = []
    for key in relations_and_ranked_papers:
        value = relations_and_ranked_papers[key]
        if papers[i]["PaperDOI"] in value:
            # print(relationships[key])
            papers[i]["Relations"].append(relationships[key])

    print("Paper titled", papers[i]["PaperTitle"][:50], "Matched with", len(papers[i]["Relations"]), "relations.")


with open("../evaluations/test_inputs/output.json", "w") as f:
    data_out = json.dumps(papers)
    f.write(data_out)