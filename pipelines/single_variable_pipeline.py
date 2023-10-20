import langchain as lc
import openai
import pathlib
import os

from dotenv import load_dotenv
load_dotenv()
key = os.getenv("OPENAI_API_KEY")

# Configure OpenAI API key
openai.api_key = key
PAPER_SOURCE = pathlib.Path("papers")

class MyMapReduceChain():
    def map(self, document):
        # If document is longer than 5000 tokens, summarize it
        if len(document.split()) > 5000:
            response = openai.Completion.create(
                engine="davinci",
                prompt=f"Summarize the following text focusing on relationships: {document}",
                max_tokens=150  # Adjust as needed
            )
            summary = response['choices'][0]['text'].strip()
            print("GPT used")
            return summary
        return document

    def reduce(self, documents):
        # Combine documents (summaries) into one text
        return ' '.join(documents)

def extract_relationships(text, variable_one, variable_two):
    # Apply MapReduce to the text
    # mr_chain = MyMapReduceChain()
    # processed_text = mr_chain.map(text)
    processed_text = text

    # Extract Relationship
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=(
            f"Given the text, identify the relationship between {variable_one} "
            f"and {variable_two}. The relationship can only be 'direct', 'inverse', "
            f"or 'inconclusive'. Text: {processed_text}"
        ),
        max_tokens=50
    )
    relationship = response['choices'][0]['text'].strip()

    # Check if a relationship was identified
    if relationship in ['direct', 'inverse', 'inconclusive']:
        # Text Citation
        start_idx = processed_text.find(variable_one)
        end_idx = processed_text.find(variable_two) + len(variable_two)
        supporting_text = processed_text[start_idx:end_idx]

        # Output Formation
        output = {
            "VariableOneName": variable_one,
            "VariableTwoName": variable_two,
            "RelationshipClassification": relationship,
            "SupportingText": supporting_text
        }
        return output

    return None  # Return None if no relationship was identified

# Example Usage:
with open(PAPER_SOURCE / "EpidemiologyandEtiologyofSubstance_10.3109_00952990.2012.694527.txt") as f:
    text = f.read()
variable_one = "Demographic"
variable_two = "epidemiological patterns of substance use"
output = extract_relationships(text, variable_one, variable_two)
print(output)
