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
PAPER_SOURCE = pathlib.Path("papers")
OUTPUTS_SOURCE = pathlib.Path("outputs")

# Configure output parser classes
class SingleRelation(BaseModel):
    VariableOneName: str
    VariableTwoName: str
    RelationshipClassification: str
    SupportingText: str

    @validator("RelationshipClassification")
    def question_ends_with_question_mark(cls, field):
        if field.lower() in {"direct", "inverse", "inconclusive"}:
            return field
        else:
            raise ValueError(f"Invalid Relationship Type {{{field}}}")

def extract_relationships(text, variable_one, variable_two):
    # Add map reduce or some other type of summarization function here.
    processed_text = text

    # Create Parser
    parser = PydanticOutputParser(pydantic_object=SingleRelation) #Refers to a class called SingleRelation

    # Create the plain text prompt, using some of langchain's functions to automatically create formatting prompts.
    query= f"""Given the text, identify the relationship between {variable_one} 
        and {variable_two}. The relationship can only be 'direct', 'inverse', 
        or 'inconclusive'. The SupportText field of your output should include a section 
        of verbatim from the text in addition to any comments you want to make about your output.
        Use exactly wording of outputs choices and input variable names, including capitalization.
        """
        # The format of the output should 
        # be a json of the form: 
        # {{
        # "VariableOneName": "variable_one",
        # "VariableTwoName": "variable_two",
        # "RelationshipClassification": "relationship",
        # "SupportingText": "supporting_text"
        # }}
    prompt = PromptTemplate(
        template = "{text}\n\n{query}\n\n{format_instructions}\n\n",
        input_variables=["query", "text"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    input_text = prompt.format_prompt(query=query, text=processed_text).to_string()
    with open(OUTPUTS_SOURCE / "SingleVariablePipelineInput.txt", "a") as f:
        f.write("Input begins:\n")
        f.write(input_text)
        f.write("\n\n\n")
    human_message_prompt = HumanMessagePromptTemplate(prompt=prompt)
    print("what is human_message_prompt:", type(human_message_prompt))
    chat_prompt = ChatPromptTemplate.from_messages([human_message_prompt])
    print("what is chat_prompt:", type(chat_prompt))

    # Get an output from the LLM
    model = ChatOpenAI(temperature=.3, openai_api_key=key, model_name="gpt-3.5-turbo-16k")
    print("What is a chat_prompt.format_prompt().to_messages():", type(chat_prompt.format_prompt(query=query, text=processed_text).to_messages()[0]))
    output = model(chat_prompt.format_prompt(query=query, text=processed_text).to_messages())
    print("what is a output:", type(output), output.content)
    with open(OUTPUTS_SOURCE / "SingleVariablePipelineOutput.txt", "a") as f:
        f.write("pre parse: ")
        f.write(str(output.content))
        f.write("\n")
    output = parser.parse(output.content)
    return output

    # Return None if no relationship was identified

# Usage:
with open(PAPER_SOURCE / "EpidemiologyandEtiologyofSubstance_10.3109_00952990.2012.694527.txt") as f:
    text = f.read()
variable_one = "Demographic"
variable_two = "epidemiological patterns of substance use"
output = extract_relationships(text, variable_one, variable_two)
with open(OUTPUTS_SOURCE / "SingleVariablePipelineOutput.txt", "a") as f:
    f.write("successful parse: ")
    f.write(str(output))
    f.write("\n")