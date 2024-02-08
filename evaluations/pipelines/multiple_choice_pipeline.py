import torch
import numpy as np
from transformers import LongformerTokenizer, LongformerForMultipleChoice

def prepare_answering_input(
        tokenizer, # longformer_tokenizer
        question,  # str
        options,   # List[str]
        context,   # str
        max_seq_length=4096,
    ):
    c_plus_q   = context + ' ' + tokenizer.bos_token + ' ' + question
    c_plus_q_4 = [c_plus_q] * len(options)
    tokenized_examples = tokenizer(
        c_plus_q_4, options,
        max_length=max_seq_length,
        padding="longest",
        truncation=True,
        return_tensors="pt",
    )
    input_ids = tokenized_examples['input_ids'].unsqueeze(0)
    attention_mask = tokenized_examples['attention_mask'].unsqueeze(0)
    example_encoded = {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
    }
    return example_encoded

# What if we can make GRADCAM for LLMs that allows us to see whether something is the case.

tokenizer = LongformerTokenizer.from_pretrained("potsawee/longformer-large-4096-answering-race")
model = LongformerForMultipleChoice.from_pretrained("potsawee/longformer-large-4096-answering-race")

context = r"""Importantly, individuals assigned to the rumination condition received higher rumination scores than participants in the cognitive distraction condition in both theMDD, F(1, 40)=54.25, p<.001, η2=0.59, and CTL group, F(1, 44)=18.73, p<.001, η2=0.30.
""".replace("\n", "")
question = r"""Relationships between variables can only be 'direct', 'inverse', 'not applicable', or 'uncorrelated'.
  Direct means that an increase in one would cause a decrease in another, and inverse means that an increase in one would cause a decrease in another.
  Uncorrelated means there is no clear relationship between the two variables. Not applicable means the text does not suggest anything about the relationship between the two variables. 
  Determine what the text implies about the relationship between Cognitive distraction -> Rumination, namely if the relation is 'direct', 'inverse', 'not applicable', or 'uncorrelated'.
  """
options  = ['direct', 'inverse', 'not applicable', 'uncorrelated']

inputs = prepare_answering_input(tokenizer=tokenizer, options=options, question=question, context=context)
outputs = model(**inputs)
prob = torch.softmax(outputs.logits, dim=-1)[0].tolist()
selected_answer = options[np.argmax(prob)]

print(dict(zip(options,prob)))
print(selected_answer)