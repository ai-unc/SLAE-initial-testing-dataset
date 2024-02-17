import yaml
import pathlib
import json
from matcher.matcher import match_relations_to_papers
from pipelines.captured_relations_pipeline import extract_relationships
from pipeline_parser.parser import pipeline_to_kumu
from kumu_to_pipeline.parser import kumu_to_pipeline


#Debug
if False:
    with open(pathlib.Path("./test_inputs/test_input.json"), "r") as f:
        to_kumu_dict = json.load(f)
    pipeline_to_kumu(to_kumu_dict, "./test_inputs/test_input_from_kumu.json")


# Obtain list of relations from Kumu or Vensim file
if False:
    with open(pathlib.Path("./test_inputs/test_input.json"), "r") as f:
        kumu_read = kumu_to_pipeline(f)
    print(kumu_read)


# Use the matcher to separate the list of relations, resulting in a series of python dictionaries each with a single paper and a list of related relations.
matched_papers = match_relations_to_papers(papers_directory="./auto_generated_inputs", input_relations_directory="./test_inputs/test_input.json")
# print(matched_papers)


# Obtain settings by reading in the file
with open("./pipeline_settings.yaml", "r") as f:
    pipeline_settings = yaml.safe_load(f)
    verbose = pipeline_settings["verbose"]
    prompt = pipeline_settings["prompt"]
    model = pipeline_settings["model"]


# For each dictionary run the "extract_relationships" function and settings
outputs = list()
for data in matched_papers:
    if len(data["Relations"]) == 0: 
        print("\nPaper", data["PaperTitle"][:50], ": no matching relations") 
        continue
    else:
        print("\nParsing", len(data["Relations"]), "relations from", data["PaperTitle"][:50])
    output = extract_relationships(data, set_prompt=prompt, verbose=verbose, model=model, outputs_source=pathlib.Path("./pipelines/debug_outputs"))
    output["PaperTitle"] = data["PaperTitle"]
    output["PaperDOI"] = data["PaperDOI"]
    # print(output["PaperDOI"])
    outputs.append(output)
    # print(outputs)
outputs_dict = {"Papers" : outputs}
debug = True
if debug:
    with open(pathlib.Path("./pipelines/debug_outputs") / "MultiVariablePipelineOutputs.json", "w") as f:
        f.write(json.dumps(outputs_dict))
    with open(pathlib.Path("./pipelines/debug_outputs") / "MultiVariablePipelineOutputs.json", "r") as f:
        outputs_dict = json.load(f)

# Obtain the list of output jsons from the iterative running of extract_relationships and recombine the output jsons into the format required to output to Kumu


# Parse it into Kumu form and save the json in a file. 