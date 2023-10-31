from pprint import pprint
import pathlib
PAPERS_PATH= pathlib.Path("papers")
INPUTS_PATH = pathlib.Path("inputs")

from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.pydantic_v1 import BaseModel, Field, validator
from pydantic import field_validator, ValidationInfo
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

key = "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" 
openai.api_key = key

PAPER_SOURCE = pathlib.Path("papers")
OUTPUTS_SOURCE = pathlib.Path("outputs")

model = ChatOpenAI(temperature=.3, openai_api_key=key, model_name="text-davinci-003") 
        
class Variable_Relationship_Extraction(BaseModel):
    # relation: dict = {
    #     "VariableOneName": str,
    #     "VariableTwoName": str,
    #     "RelationshipClassification": str,
    #     "SupportingText": str
    # }
    VariableOneName: str
    VariableTwoName: str
    RelationshipClassification: str
    SupportingText: str

    @field_validator('RelationshipClassification')
    @classmethod
    def invalid_relationship_type(cls, field: str):
        if field.lower() in {"direct", "inverse", "inconclusive"}:
            return field
        else:
            raise ValueError(f"Invalid Relationship Type {{{field}}}")

class Multivariable_List(BaseModel):
    __root__: Variable_Relationship_Extraction 
    class Config:
           schema_extra = {
               "examples": [
                   {
                       {
                           "VariableOneName": "Adolescent Grade Level",
                            "VariableTwoName": "Adolescent Drinking",
                            "RelationshipClassification": "Direct",
                            "SupportingText": "In all models, grade level was positively associated with adolescent drinking (positive coefficients, e.g., b = 0.192, p < 0.001 in Model 3)."},
                        {
                            "VariableOneName": "Peer Drinking",
                            "VariableTwoName": "Adolescent Drinking",
                            "RelationshipClassification": "Direct",
                            "SupportingText": "In Model 1 and Model 2, peer drinking significantly predicted adolescent drinking at Wave II, with a positive coefficient (b = 0.061, p < 0.05)."
                       }
                   }
               ]
           }
    

def extract_relationships(text, verbose = False):
    processed_text = text
    parser = PydanticOutputParser(pydantic_object=Multivariable_List)
    # example 1 general case, example 2 edge case
    query= f"""Given the text, identify relationships between variables. The RelationshipClassification field can only be 'direct', 'inverse', 
        or 'inconclusive'. The SupportText field should be a direct quote from the text explaining the reasoning for the classification of the relationship.
        Use exactly wording of outputs choices and input variable names, including capitalization.
        The output should be in the following json format:
        {{"VariableOneName": "Consistent birth control use over a 5-year period or more",
		"VariableTwoName": "AEP",
		"RelationshipClassification": "Inverse",
		"SupportingText": "Individuals who used birth control more consistently over the 5-year period compared to other individuals decreased odds of AEP by 66% (compared to non-pregnancy) and 62% (compared to nAEP)."}},
        {{"VariableOneName": "Incarceration",
        "VariableTwoName": "Black men mortality",
        "RelationshipClassification": "Inconclusive",
        "SupportingText": "In spite of the growing body of research demonstrating the negative health implications of incarceration, there is increasing evidence that incarceration has a protective effect on mortality rates for black men. Using national-level data, Mumola (2007) found that the mortality rate for black male prisoners aged 15–64 was 19% lower than that for black men in the general population. Patterson's (2010) results also revealed that the substantial inequality in mortality rates for blacks and whites in the general population largely disappeared in the incarcerated population. She found that whereas the within-prison mortality rate for white males was higher than the rate for white males in the general population, the within-prison mortality rate for black males was considerably lower than the rate for black males in the general population. Similarly, using standardized mortality ratios to compare death rates of males in North Carolina prisons with expected death rates based on state residents, Rosen et al. (2011) found 48% fewer deaths than expected among black prisoners. Another study, however, suggests an alternative explanation. The practice of compassionate release, i.e., releasing inmates who are in particularly poor health and close to death, is not uncommon in some states. Compassionate release reduces the mortality rate of the incarcerated population and increases the mortality rate of the comparable resident population. In their study of mortality among current and former Georgia prisoners, Spaulding et al. (2011) initially found a substantially lower mortality rate among incarcerated black men relative to nonincarcerated black men. After controlling for the compassionate release of moribund prisoners, however, the effect disappeared."}}"""
    prompt = PromptTemplate(
        template = """{text}\n\n{query}\n\n{format_instructions}\n\n""",
        input_variables=["query", "text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}, 
    )
    input_text = prompt.format_prompt(query=query, text=processed_text).to_string()
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
    completion_prompt = chat_prompt.format_prompt(query=query, text=processed_text).to_messages()
    if verbose:
        print("What is a completion_prompt:", type(completion_prompt))
    
    output = model(extract_relationships(input_text))
    parser.parse(output)
    #json serializer




