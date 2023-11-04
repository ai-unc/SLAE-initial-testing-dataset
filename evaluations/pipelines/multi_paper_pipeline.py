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

# Configure constants
PAPER_SOURCE = pathlib.Path("../../papers")
OUTPUTS_SOURCE = pathlib.Path("../../outputs")

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

def extract_relationships(text, variable_one, variable_two, verbose = False):
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
        The SupportText field of your output should include a section of verbatim from the text in addition to any comments you want to make about your output.
        Use exactly wording of outputs choices and input variable names, including capitalization choices.

        {format_instructions}
        """,
        input_variables=["text"],
        partial_variables={"format_instructions":parser.get_format_instructions}
    )
    input_text = prompt.format_prompt(text=processed_text).to_string()
    if verbose:
        with open(OUTPUTS_SOURCE / "SingleVariablePipelineInput.txt", "a") as f:
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
    model = ChatOpenAI(temperature=.3, openai_api_key=key, model_name="gpt-3.5-turbo-16k")

    # Obtain completion from LLM
    output = model(completion_prompt)
    if verbose:
        print("what is a output:", type(output), output.content)
        with open(OUTPUTS_SOURCE / "SingleVariablePipelineOutput.txt", "a") as f:
            f.write("pre parse: ")
            f.write(str(output.content))
            f.write("\n")
    output = parser.parse(output.content)
    return output

if __name__ == "__main__":
    # Prepare inputs:
    text = str()
    with open(PAPER_SOURCE / "testpaper.txt") as f:
        text = f.read()
    variable_one = "AI/AN status"
    variable_two = "Substance use"

    # Process and save outputs:
    output = extract_relationships(text, variable_one, variable_two, verbose=True)
    with open(OUTPUTS_SOURCE / "SingleVariablePipelineOutput.txt", "a") as f:
        f.write("successful parse MULTIRELATION: ")
        f.write(output.json())
        f.write("\n")