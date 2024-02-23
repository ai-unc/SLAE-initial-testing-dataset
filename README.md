# SLAE Initial Testing Dataset

### Contains text & pdf files of initial papers used purely for testing and prototyping + corresponding json input files

## Description

This project involves the development of pipelines to evaluate relationships within academic texts, specifically focusing on the identification and classification of variable relationships. The project's structure includes directories and code for evaluation outputs, pipelines, and dataset management.

## File Structure

- `evaluations/`
  - This directory contains evaluation outputs, the pipeline implementations for single and multi-paper evaluations, and datasets for evaluations.
  - `evaluation_outputs/`
    - Stores results, predictions, and other relevant information from evaluations.
  - `pipelines/`
    - Contains Python scripts that define the evaluation pipelines.
  - `evaluation_datasets/`
    - Houses datasets used for evaluating the pipelines in both single and multi-relation contexts.

## Pipelines

### Single Variable Pipeline

The `single_variable_pipeline.py` file within the `evaluations/pipelines/` directory contains the implementation of a pipeline designed to identify and evaluate the relationship between two variables within a text.

### Multi Paper Pipeline

The `multi_paper_pipeline.py` file handles the extraction of relationships from multiple papers, leveraging the Langchain library and OpenAI's GPT models for processing and evaluation.

### Evaluators

- `single_relation_evaluator.py` and `multi_relation_evaluator.py`
  - These scripts are used to calculate scores based on predictions and ground truth data for the single and multiple relationship identification tasks.

## Usage

To use the evaluation pipelines, follow the instructions in the `single_variable_pipeline.py` or `multi_paper_pipeline.py` files for setting up the environment and running the scripts. The evaluators can be run similarly, using the datasets provided in the `evaluation_datasets/` directory.

## Dependencies

- langchain
- pydantic
- openai
- dotenv

Make sure to install these dependencies before running the pipelines.

## Adding a paper

There is a python script to quickly rename a paper file and create a corresponding json file.

### Usage
Ensure that the only map in your project is the map you want to verify using SLAE. 
You can export a single map with this utility: https://to-kumu-map-blueprint.netlify.app/.
Rename the file "user_input.json".
Run the "flow_control.py" script!
Start a new kumu project and make an empty Causal Loop Diagram map.
Import the file "final_to_kumu_output.json" into the project.
Open the right hand side settings bar and switch to Advanced Settings Mode.
Replace existing code with the following:

@settings {
  template: causal-loop;
  layout: force;
  layout-preset: dense;
  connection-size: 6;
  connection-curvature: 0.28;
}

/* Correctness */
connection {
  color: scale("correctness", #FF2D00, #FF9B85);
}

/* Papers Examined */
connection {
  scale: scale("papers examined", 1, 2);
}

#### Example:

```py
python script.py
-file="paper.txt"
-doi="10.1111/j.1460-9568.2012.08013.x"
-title="Orexin / hypocretin 1 receptor antagonist reduces heroin self-administration and cue-induced heroin seeking"
```

**You will need to manually add the variable relationships to the input json file**

You can use the following commands for usage help:
```py
python script.py -h
python script.py --help
``` 

## Parsing .mdl Files

There is a python script to parse the .mdl files into .json files, one for general use and the other for Kumu. This script and it's documentation can be found in the "parser" directory. 

## Acknowledgments

This project utilizes the Langchain library and OpenAI's GPT models for processing academic texts.