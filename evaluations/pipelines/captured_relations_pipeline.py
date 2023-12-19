import langchain as lc
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.pydantic_v1 import BaseModel, Field, validator
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import openai
import pathlib
import os
import json
from pprint import pprint
import yaml

# Configure OpenAI API key
from dotenv import load_dotenv
load_dotenv()
key = os.getenv("OPENAI_API_KEY")
openai.api_key = key

# Filepath Debug
mypath = os.path.abspath("")
print("___\n\n\n", mypath)

# Configuration
"""This section configs the run"""
with open("./pipeline_settings.yaml", "r") as f:
    settings = yaml.safe_load(f)
PAPER_SOURCE = pathlib.Path("../papers")
INPUTS_SOURCE = pathlib.Path("../inputs")
OUTPUTS_SOURCE = pathlib.Path("../outputs")
DATASET_PATH = pathlib.Path("evaluation_datasets/multi_relation_dataset")
PAPER_FILENAME = "RuminationandCognitiveDistractionin_10.1007_s10862_015_9510_1.json"
MODEL_NAME = "gpt-3.5-turbo-1106"
        
class SingleRelation(BaseModel):
    VariableOneName: str
    VariableTwoName: str
    SupportingText: str
    Reasoning: str
    RelationshipClassification: str
    # IsCausal: str
    
    @validator("RelationshipClassification")
    def allowed_classifications(cls, field):
        if field.lower() in {"direct", "inverse", "not applicable", "uncorrelated"}:
            return field
        else:
            raise ValueError(f"Invalid Relationship Type {{{field}}}")
        
    # @validator("IsCausal")
    # def true_or_false(cls, field):
    #     if field.lower() in {"true", "false"}:
    #         return field
    #     else:
    #         raise ValueError(f"Invalid IsCausal Type {{{field}}}")

class ListOfRelations(BaseModel):
    Relations: list[SingleRelation]

# CWD switcher to ensure that the verbose option works when it is being run from the captured relations evaluator file
import os
import inspect

class WorkingDirectoryManager:
    def __init__(self):
        self.original_directory = os.getcwd()

    def change_to_module_directory(self):
        module_file_path = inspect.getfile(inspect.currentframe())
        module_dir = os.path.dirname(os.path.abspath(module_file_path))
        os.chdir(module_dir)

    def restore_original_directory(self):
        os.chdir(self.original_directory)

def extract_relationships(data, verbose = False, model = "gpt-4", verbatim=False):
    """
    12/19/2023 (Function Last Updated)
    Data should be a python dictionary cleaned of all ground truth data. 
    Verbose triggers storage of information into debug files, this may break depending on where you run this script from as it depends on relative paths.
    Model specifies LLM to be used. (This file was only tested with OpenAI LLMs)
    Verbatim feeds the exact formatting of the dictionary found in the ground truth encoding into the prompt. (Minus the ground truth data)
    Verbatim will make it hard for the model to decide whether or not to include fields that were not in ground truth if you modify the SingleRelation class.
    """
    # Add map reduce or some other type of summarization function here.
    processed_text = data["PaperContents"]
    if verbatim:
        relationships = {"Relations": data["Relations"]}
    else:
        relationships = extract_all_ordered_pairs(data)

    # Create Parser
    parser = PydanticOutputParser(pydantic_object=ListOfRelations) #Refers to a class called SingleRelation

    # Create the plain text prompt. Used some of langchain's functions to automatically create formated prompts. 
    prompt = PromptTemplate(
        template="""
START TEXT
{text}
END TEXT

START PROMPT
Given the text validate a series of relationships between variables that will be included in a json format below.
For example, if the json includes a relation like "Country's per capita income -> Country's literacy rate", and the text includes "We find a strong correlation p < .0001 between a country's per capita income and it's literacy rate" then the RelationshipClassification would be direct.
If instead the text includes ""We find a strong inverse correlation p < .0001 between a country's per capita income and it's literacy rate" then the RelationshipClassification would be inverse.
The SupportText field of your output should include verbaitum text related to the relation between the two variables without paraphrasing.
The Reasoning field should be used to step by step reason from the text of the paper to try to come up with a good relationship classification and should focus on plainly stated results over implications.
The RelationshipClassification field can only be 'direct', 'inverse', 'not applicable', or 'uncorrelated'.
Direct means that an increase in one would cause a decrease in another, and inverse means that an increase in one would cause a decrease in another.
Uncorrelated means there is no clear relationship between the two variables. Not applicable means the text does not suggest anything about the relationship between the two variables. 
Use exactly wording of outputs choices and input variable names, including capitalization choices. 

OUTPUT FORMATTING INSTRUCTIONS START
{format_instructions}
OUTPUT FORMATTING INSTRUCTIONS END

Below is the list of relationships that you should include in your output. Ensure all relationships are evaluated!
{relationships}
End of the list of relationships.

END PROMPT
        """,
        input_variables=["text", "relationships"],
        partial_variables={"format_instructions":parser.get_format_instructions}
    )
    input_text = prompt.format_prompt(text=processed_text, relationships=relationships).to_string()
    if verbose:
        with open(OUTPUTS_SOURCE / "MultiVariablePipelineInput.txt", "a") as f:
            f.write("Input begins:\n")
            f.write(input_text)
            f.write("\n\n\n")
    human_message_prompt = HumanMessagePromptTemplate(prompt=prompt)
    if verbose:
        print("what is human_message_prompt:", type(human_message_prompt))
    chat_prompt = ChatPromptTemplate.from_messages([human_message_prompt])
    if verbose:
        print("what is chat_prompt:", type(chat_prompt))
    completion_prompt = chat_prompt.format_prompt(text=processed_text, relationships=relationships).to_messages()
    if verbose:
        print("What is a completion_prompt:", type(completion_prompt))

    # Create LLM
    model = ChatOpenAI(temperature=.0, openai_api_key=key, model_name=model)

    # Obtain completion from LLM
    output = model(completion_prompt)
    if verbose:
        print("what is a output:", type(output))
        with open(OUTPUTS_SOURCE / "MultiVariablePipelineOutput.txt", "a") as f:
            f.write("pre parse: ")
            f.write(str(output.content))
            f.write("\n")
    parsed_output = parser.parse(output.content) # Ensure content is in valid json format.
    return parsed_output.dict()  # Returns in dict format

def clean_data(data_file, verbose=False) -> dict():
    """Reads Json and removes paper fulltext and list of user predictions"""
    with open(data_file, "r") as f:
        data = json.load(f)
    for relation in data['Relations']:
        relation["RelationshipClassification"] = ""
        relation["IsCausal"] = ""
        relation["SupportingText"] = ""
        relation["Attributes"] = ""
    if verbose:
        pprint(data)
    return data  

def extract_all_ordered_pairs(data):
    #Extract the relationships
    relationships = data.get("Relations", [])
    variable_pairs = [f"Below are {len(relationships)} relations:"]
    # Iterate through each relationship and extract variables
    for relationship in relationships:
        variable_one = relationship.get("VariableOneName", "")
        variable_two = relationship.get("VariableTwoName", "")
        variable_pairs.append(variable_one + " -> " + variable_two)
    relations_text = "\n".join(variable_pairs)
    return relations_text


def match_relation_to_paper():
    """Reference passage ranking section https://huggingface.co/tasks/sentence-similarity"""
    pass

def obtain_papers_via_MLSE():
    """Obtains relevant papers via the massive literature search engine"""
    pass

def captured_relations_pipeline(data_file=DATASET_PATH/PAPER_FILENAME, verbose=False, model=MODEL_NAME):
    cleaned_data = clean_data(data_file, verbose=verbose)
    output = extract_relationships(cleaned_data, verbose=verbose, model=model)
    return output

if __name__ == "__main__":
    # # Prepare inputs:
    # data = clean_data(INPUTS_SOURCE/"IncarcerationandHealth_10.1146_annurev_soc_073014_112326.json")
    
    # # # Process and save outputs:
    # output = extract_relationships(data, verbose=True)
    # with open(OUTPUTS_SOURCE / "MultiVariablePipelineOutput.txt", "a") as f:
    #     f.write("successful parse MULTIRELATION: ")
    #     f.write(str(output))
    #     f.write("\n")
    pass