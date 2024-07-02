# Have issues loading the GGUF - likely my download
#  - will try again once I've though this through more

# Imports
import os
from llama_cpp import Llama
import urllib.request

# Retrieve the model from the Hugging Face hub
file_path = "./model.gguf"
if not os.path.exists(file_path):
    print("Downloading north-llama3-v0.01.gguf, please wait a short while...")
    url = "https://huggingface.co/north/north-llama3-8b-ggml/resolve/main/north-llama3-v0.01.gguf?download=true"
    urllib.request.urlretrieve(url, file_path)
    print("north-llama3-v0.01.gguf downloaded successfully.")
else:
    print("[north-llama3-v0.01.ggufis available locally.]")

# Load the model
llm = Llama(
    model_path=file_path,
    n_ctx=16000,
    n_threads=32,
    n_gpu_layers=0
)

# Set the prompt
prompt = "The meaning of life is "
prompt_template=f'''SYSTEM: You are a helpful, respectful and honest assistant. Always answer as helpfully.

USER: {prompt}

ASSISTANT:
'''
generation_kwargs = {
    "max_tokens": 20000,
    "stop": ["</s>"],
    "echo": False,  # Echo the prompt in the output
    "top_k": 1  # Greedy decoding (highest-probability token)
}

# Get the response
response=llm(prompt, **generation_kwargs)
print(response);
print(response["choices"][0]["text"])