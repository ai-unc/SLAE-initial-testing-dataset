import yaml
import pathlib
from matcher.matcher import match_relations_to_papers
from pipelines.captured_relations_pipeline import extract_relationships

# Obtain list of relations from Kumu or Vensim file



# Use the matcher to separate the list of relations, resulting in a series of python dictionaries each with a single paper and a list of related relations.
matched_papers = match_relations_to_papers(papers_directory="./auto_generated_inputs", input_relations_directory="./test_inputs/test_input.json")
print(matched_papers)


# Obtain settings by reading in the file
with open("./pipeline_settings.yaml", "r") as f:
    pipeline_settings = yaml.safe_load(f)
    verbose = pipeline_settings["verbose"]
    prompt = pipeline_settings["prompt"]
    model = pipeline_settings["model"]


# For each dictionary run the "extract_relationships" function and settings
for data in matched_papers:
    output = extract_relationships(data, set_prompt=prompt, verbose=verbose, model=model, outputs_source=pathlib.Path("./pipelines/debug_outputs"))


# Obtain a list of output jsons from the iterative running of extract_relationships

# Recombine the output jsons into the format required to output to Kumu

# Parse it into Kumu form and save the json in a file. 