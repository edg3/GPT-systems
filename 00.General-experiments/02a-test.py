# Shows results of the model trained on the sample dataset
#  - too low, needs more work on model training

from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

model_name = 'gpt2'
device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

# Load the trained model
model = GPT2LMHeadModel.from_pretrained(model_name)
model.load_state_dict(torch.load('sample.safetensor'))
model.to(device)
model.eval()

# Send a message and get the generated response
message = "Make a data type in latest C# that has get and set for different data types for lost and found"
input_ids = tokenizer.encode(message, return_tensors='pt').to(device)
output = model.generate(input_ids=input_ids, max_length=1024)
response = tokenizer.decode(output[0], skip_special_tokens=True)

print("Generated response:", response)