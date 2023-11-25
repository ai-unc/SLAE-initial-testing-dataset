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
PAPER_SOURCE = pathlib.Path("../../papers")
INPUTS_SOURCE = pathlib.Path("../../inputs")
OUTPUTS_SOURCE = pathlib.Path("../../outputs")
PAPER_FILENAME = "IncarcerationandHealth_10.1146_annurev_soc_073014_112326.text"
MODEL_NAME = "gpt-3.5-turbo-1106"
        
class SingleRelation(BaseModel):
    VariableOneName: str
    VariableTwoName: str
    RelationshipClassification: str
    isCausal: str
    SupportingText: str
    

    @validator("RelationshipClassification")
    def question_ends_with_question_mark(cls, field):
        if field.lower() in {"direct", "inverse", "not applicable", "independent"}:
            return field
        else:
            raise ValueError(f"Invalid Relationship Type {{{field}}}")

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

def extract_relationships(data, verbose = False, model = "gpt-3.5-turbo-1106"):
    # Add map reduce or some other type of summarization function here.
    processed_text = data["PaperContents"]
    relationships = data["Relations"]

    # Create Parser
    parser = PydanticOutputParser(pydantic_object=ListOfRelations) #Refers to a class called SingleRelation

    # Create the plain text prompt. Used some of langchain's functions to automatically create formated prompts. 
    # formatting_text = """
    # The output should be formatted as a JSON instance that conforms to the JSON schema below.

    # As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
    # the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

    # Here is the output schema:
    # ```
    # {"Relationships":[{"properties": {"VariableOneName": {"title": "Variableonename", "type": "string"}, "VariableTwoName": {"title": "Variabletwoname", "type": "string"}, "Reasoning": {"title": "Reasoning", "type": "string"}, "RelationshipClassification": {"title": "Relationshipclassification", "type": "string"}, "isCausal": {"title": "Iscausal", "type": "string"}, "SupportingText": {"title": "Supportingtext", "type": "string"}}, "required": ["VariableOneName", "VariableTwoName", "RelationshipClassification", "isCausal", "SupportingText"]}]}
    # ```"""
    prompt = PromptTemplate(
        template="""
        {text}

        Given the text validate a series of relationships between variables that will be included in a json format below.
        For example, if the json includes a relation between "Country's per capita income" and "Country's literacy rate", and the text includes "We find a strong correlation p < .0001 between a country's per capita income and it's literacy rate" then the RelationshipClssification would be direct.
        The RelationshipClassification field can only be 'direct', 'inverse', 'Not applicable', or 'independent'.
        The isCausal field can only be either 'True' or 'False', and can only be true if the text directly states that the relationship is a causal relationship.
        The SupportText field of your output should include verbaitum text related to the relation between the two variables without paraphrasing.
        Use exactly wording of outputs choices and input variable names, including capitalization choices. 
        
        {format_instructions}

        Below is a list of relationships, please fill in the fields according to the above instructions.
        {relationships}
        End of relationships to fill in.
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
    model = ChatOpenAI(temperature=.3, openai_api_key=key, model_name=model)

    # Obtain completion from LLM
    output = model(completion_prompt)
    if verbose:
        print("what is a output:", type(output), output.content)
        with open(OUTPUTS_SOURCE / "MultiVariablePipelineOutput.txt", "a") as f:
            f.write("pre parse: ")
            f.write(str(output.content))
            f.write("\n")
    parsed_output = parser.parse(output.content) # Ensure content is in valid json format.
    return parsed_output.dict()  # Returns in dict format

def clean_data(data_file, verbose=False) -> dict():
    """Reads Json and cleans all information into a dict, including paper fulltext and list of user predictions"""
    with open(data_file, "r") as f:
        data = json.load(f)
    for relation in data['Relations']:
        relation["RelationshipClassification"] = ""
        relation["isCausal"] = ""
        relation["SupportingText"] = ""
    if verbose:
        pprint(data)
    return data  

def match_relation_to_paper():
    """Reference passage ranking section https://huggingface.co/tasks/sentence-similarity"""
    pass

def obtain_papers_via_MLSE():
    """Obtains relevant papers via the massive literature search engine"""
    pass

def captured_relations_pipeline(data_file, verbose=False, model="gpt-3.5-turbo-1106"):
    cleaned_data = clean_data(data_file, verbose=verbose)
    output = extract_relationships(cleaned_data, verbose=verbose, model=model)
    return output

if __name__ == "__main__":
    # # Prepare inputs:
    data = clean_data(INPUTS_SOURCE/"IncarcerationandHealth_10.1146_annurev_soc_073014_112326.json")
    
    # # Process and save outputs:
    output = extract_relationships(data, verbose=True)
    with open(OUTPUTS_SOURCE / "MultiVariablePipelineOutput.txt", "a") as f:
        f.write("successful parse MULTIRELATION: ")
        f.write(str(output))
        f.write("\n")