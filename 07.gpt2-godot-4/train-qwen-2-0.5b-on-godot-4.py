# Step 1: pip install torch transformers Flask datasets sentencepiece torchvision torchaudio jinja2 tensorflow==2.19.0 tf-keras==2.19.0 accelerate>=0.26.0
# Step 2: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 
#         pip install transformers datasets sentencepiece
#         pip install Flask jinja2  # For deployment
# Step 3: Load datasets into training list
import os
# Suppress TensorFlow oneDNN warning
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
# Suppress TensorFlow deprecation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

# Stop verbose TensorFlow warnings error only
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)    # Generate output with attention mask and explicitly set pad_token_id

import json
newList = {}

import time
start_time = time.time()

# Mode = 0 => all; Mode = 1 => glaiveai/godot_4_docs; Mode = 2 => minosu/godot_dodo_4x_60k; Mode = 3 => dotfantasy/godot-code
mode = 0
train_size = 30

from datasets import load_dataset

if mode == 1 or mode == 0:
    # Load the Hugging Face dataset 'glaiveai/godot_4_docs'
    dataset_1 = load_dataset('glaiveai/godot_4_docs')
    oldList_1 = [item for item in dataset_1['train']]
    print(oldList_1[0])
    for i in range(len(oldList_1)):
        p = oldList_1[i]['prompt']
        a = oldList_1[i]['response']
        #if (len(p) + len(a) > 512) and (len(p) + len(a) < 1024):
        newList[i] = {"prompt": p, "code": a}
if mode == 2 or mode == 0:
    # Load the Hugging Face dataset 'minosu/godot_dodo_4x_60k'
    dataset_2 = load_dataset('minosu/godot_dodo_4x_60k')
    oldList_2 = [item for item in dataset_2['train']]
    print(oldList_2[0])
    for i in range(len(oldList_2)):
        p = oldList_2[i]['instruction']
        a = oldList_2[i]['output']
        #if (len(p) + len(a) > 512) and (len(p) + len(a) < 1024):
        newList[i] = {"prompt": p, "code": a}
if mode == 3 or mode == 0:
    # Load the Hugging Face dataset 'dotfantasy/godot-code'
    dataset_3 = load_dataset('dotfantasy/godot-code')
    oldList_3 = [item for item in dataset_3['train']]
    print(oldList_3[0])
    for i in range(len(oldList_3)):
        p = oldList_3[i]['instruction']
        a = oldList_3[i]['output']
        #if (len(p) + len(a) > 512) and (len(p) + len(a) < 1024):
        newList[i] = {"prompt": p, "code": a}

print(newList[0])

with open('./data.jsonl', 'w') as f:
    for item in newList.values():
        json.dump(item, f)
        f.write('\n')

# Print the time elapsed since start_time
elapsed_time = time.time() - start_time
print(f"Time elapsed to load data: {elapsed_time:.2f} seconds")
start_time = time.time()

# Step 4: Load and tokenise the dataset
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling,
)
from datasets import load_dataset
import os
from safetensors.torch import load_file
 
# Load pre-trained model and tokenizer
model_name = 'openai-community/gpt2' # Licence: MIT ; 1024 tokens

# Check if the model file exists to continue training on, and load it if available
model_path = "model/model.safetensors"
if os.path.exists(model_path):
    model_name = 'model'
else:
    print(f"Model file {model_path} not found. Using pre-trained model {model_name}")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, ignore_mismatched_sizes=True)
tokenizer.pad_token = tokenizer.eos_token

# Move model to appropriate device
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

# After loading your model but before training
if hasattr(model.config, 'max_position_embeddings'):
    model.config.max_position_embeddings = 1024  # Match your tokenizer max_length

# For Qwen2 specifically - more explicit configuration
if hasattr(model.config, 'rope_theta'):
    model.config.rope_theta = 10000.0
    model.config.rope_scaling = None
    
    # Add this check for rope dimensions
    if hasattr(model, 'model') and hasattr(model.model, 'decoder'):
        print("Setting rotary embedding dimensions explicitly...")
        for layer in model.model.decoder.layers:
            if hasattr(layer.self_attn, 'rotary_emb'):
                # Make sure rotary dimensions are properly set
                layer.self_attn.rotary_emb.dim = 64
 
# Load your custom dataset
dataset = load_dataset('json', data_files={'train': './data.jsonl'})
print('Test last line len: ',dataset['train'][len(dataset['train']) - 1])

# Apply filter before tokenization
print('Len dataset:', len(dataset['train']))
 
# Tokenize the dataset
def tokenize_function(example):
    prompt = ''.join(example['prompt']) if isinstance(example['prompt'], list) else example['prompt']
    code = ''.join(example['code']) if isinstance(example['code'], list) else example['code']
    
    # Use return_tensors=None to avoid premature conversion to tensors
    tokens = tokenizer(
        prompt + "\n" + code,
        truncation=True,
        padding="max_length",
        max_length=1024,
        return_tensors=None
    )
    
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens
 
tokenized_datasets = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=['prompt', 'code']
)

# Print the time elapsed since start_time
elapsed_time = time.time() - start_time
print(f"Time elapsed to load model and tokenize datasets: {elapsed_time:.2f} seconds")
# Print the shape of each column in tokenized_datasets
for column in tokenized_datasets['train'].column_names:
    print(f"Column: {column}, Shape: {len(tokenized_datasets['train'][column])}")

# Step 5: Split the dataset into training and validation sets
tokenized_datasets = tokenized_datasets['train'].train_test_split(test_size=0.1)

# Step 6: Set up training arguments
training_args = TrainingArguments(
    output_dir="./model",
    num_train_epochs=train_size,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,  # Add gradient accumulation
    per_device_eval_batch_size=1,   # Reduce eval batch size
    save_steps=5000,
    save_total_limit=2,
    eval_strategy="steps",
    eval_steps=1000,
    logging_steps=500,
    load_best_model_at_end=True,
    metric_for_best_model="loss",
    greater_is_better=False,
    fp16=False,  # Disable mixed precision during debugging
)

# Data collator for language modeling
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)
 
# Step 7: Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['test'],
    data_collator=data_collator,
)

# Step 8: Train the model
start_time = time.time()
trainer.train()
elapsed_time = time.time() - start_time
print(f"Time elapsed for this training cycle: {elapsed_time:.2f} seconds")
start_time = time.time()

# Step 9: Save the model
model.save_pretrained("./model")
tokenizer.save_pretrained("./model")

# Step 10: Evaluate the model
def generate_prediction(prompt, max_length=200):
    # Get the model's device
    device = model.device
    
    # Encode the prompt
    inputs = tokenizer(prompt, return_tensors='pt', padding=True)
    
    # Move all inputs to the same device as the model
    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)
    
    output = model.generate(
        input_ids, 
        attention_mask=attention_mask,
        max_length=max_length, 
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id  # Explicitly set pad_token_id
    )
    
    # Decode and return
    return tokenizer.decode(output[0], skip_special_tokens=True)

def print_query(q):
    ans = generate_prediction(q, max_length=1024)
    print(f"Prompt: {q}\n\nResponse: {ans}\n")

print_query('How to create a new scene in Godot 4?')
print_query('What is the difference between a variable and a constant in GDScript?')
print_query('How to @export Sprite2D properly?')
print_query('Top-Down Dungeon Map: Procedural Tiles with TileMapLayer?')
print_query('How can I make my own Godot 4 dark underground lighting shader?')
