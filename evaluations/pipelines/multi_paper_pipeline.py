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
OUTPUTS_SOURCE = pathlib.Path("../../outputs")
PAPER_FILENAME = "RuminationandCognitiveDistractionin_10.1007_s10862_015_9510_1.text"
MODEL_NAME = "gpt-3.5-turbo-1106"

#I am getting an error when running this in the slae_repo/SLAE-initial-testing-dataset on Windows
#I don't wanna edit/delete this code, so I will just make another file and then test out if that work for everyone else as well
#The changes in this fily only include minor changes (ai deletion of unneccessary variables, and putting already created constants to the model)

# Configure output parser classes
class SingleRelation(BaseModel):
    VariableOneName: str
    VariableTwoName: str
    RelationshipClassification: str
    isCausal: str
    SupportingText: str

    @validator("RelationshipClassification")
    def question_ends_with_question_mark(cls, field):
        if field.lower() in {"direct", "inverse", "inconclusive"}:
            return field
        else:
            raise ValueError(f"Invalid Relationship Type {{{field}}}")

class ListOfRelations(BaseModel):
    Relations: list[SingleRelation]

def extract_relationships(text, verbose = False, model = MODEL_NAME):
    # Add map reduce or some other type of summarization function here.
    processed_text = text

    # Create Parser
    parser = PydanticOutputParser(pydantic_object=ListOfRelations) #Refers to a class called SingleRelation

    # Create the plain text prompt. Used some of langchain's functions to automatically create formated prompts. 
    formatting_text = """
    The output should be formatted as a JSON instance that conforms to the JSON schema below.

    As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
    the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

    Here is the output schema:
    ```
    {"Relationships":[{"properties": {"VariableOneName": {"title": "Variableonename", "type": "string"}, "VariableTwoName": {"title": "Variabletwoname", "type": "string"}, "RelationshipClassification": {"title": "Relationshipclassification", "type": "string"}, "isCausal": {"title": "Iscausal", "type": "string"}, "SupportingText": {"title": "Supportingtext", "type": "string"}}, "required": ["VariableOneName", "VariableTwoName", "RelationshipClassification", "isCausal", "SupportingText"]}]}
    ```"""
    prompt = PromptTemplate(
        template="""
        {text}

        Given the text identify a series of relationships between variables that have a well defined positive direction and a clear textual backing.
        For example, if a text says "We find a strong correlation p < .0001 between a country's per capita income and it's literacy rate" then "Country's per capita income" and "Country's literacy rate" would be good variables. Variables that are implied but not directly stated by the text such as "education infilstructure" should not be included. 
        The RelationshipClassification field can only be 'direct', 'inverse', 
        or 'inconclusive'. The isCausal field can only be either 'True' or 'False', and can only be true if the text directly states that the relationship is a causal relationship.
        The SupportText field of your output should include a section of verbatim from the text in addition to any comments you want to make about your output, without paraphrasing.
        Use exactly wording of outputs choices and input variable names, including capitalization choices.

        {format_instructions}
        """,
        input_variables=["text"],
        partial_variables={"format_instructions":parser.get_format_instructions}
    )
    input_text = prompt.format_prompt(text=processed_text).to_string()
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
    completion_prompt = chat_prompt.format_prompt(text=processed_text).to_messages()
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
    parsed_output = parser.parse(output.content)
    return output

if __name__ == "__main__":
    # Prepare inputs:
    text = str()
    with open(PAPER_SOURCE / "RuminationandCognitiveDistractionin_10.1007_s10862_015_9510_1.txt") as f:
        text = f.read()

    # Process and save outputs:
    output = extract_relationships(text, verbose=True, model=MODEL_NAME)
    with open(OUTPUTS_SOURCE / "MultiVariablePipelineOutput.txt", "a") as f:
        f.write("successful parse MULTIRELATION: ")
        f.write(str(output.content))
        f.write("\n")