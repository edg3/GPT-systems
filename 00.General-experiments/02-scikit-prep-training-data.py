# Isn't enough training

import json
from PyPDF2 import PdfReader # pip install PyPDF2
import os
from sklearn.model_selection import train_test_split # pip install scikit-learn
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from torch.utils.data import Dataset, DataLoader
import torch

# Load the PDF file
print('Loading PDF')
# Source: https://riptutorial.com/ebook/csharp
#          - Credits to everyone who contributed to the C# ebook
pdf_file = "csharp-language.pdf"
lstAnswers = []
reader = PdfReader(pdf_file)
for page in reader.pages:
    parts = []

    def visitor_body(text, cm, tm, fontDict, fontSize):
        y = tm[5]
        if y > 50 and y < 720 and text.find("O'Reilly") == -1 and text.find('reilly') == -1:
            parts.append(text)

    page.extract_text(visitor_text=visitor_body)
    text_body = "".join(parts)

    lstAnswers.append(text_body)

lstAnswers = lstAnswers[54:974] # doesnt account for blanks
# print(len(lstAnswers))
# print(lstAnswers[0]) # first line
# print(lstAnswers[-1]) # last line

## 1. Comment below, find the size of the lstAnswers and lose the start and end which we dont need
## 2. Comment out below, and run
##      - e.g. start line: from: csharp-language \n It is an unofficial and free C# Language ebook created for educational purposes. All the content is
##      - e.g. end line  : Read Yield Keyword online: https://riptutorial.com/csharp/topic/61/yield-keyword
# Generate a list of dictionaries
lines = []
for page in lstAnswers:
    if (len(page) > 0):
        lines.append({"len": len(page),"text": page})

# Convert to a list of JSON strings
json_lines = [json.dumps(l) for l in lines]

# Check if file exists and delete it
if os.path.exists('sampledata.jsonl'):
    os.remove('sampledata.jsonl')

print("Printing ",len(json_lines)," lines to sampledata.jsonl")
# Join lines and save to .jsonl file
json_data = '\n'.join(json_lines)
with open('sampledata.jsonl', 'w') as f:
    f.write(json_data)

# Load the lines from sampledata.jsonl
with open('sampledata.jsonl', 'r') as f:
    lines = [json.loads(line) for line in f]

# Split the lines into training, test, and validation sets
train_lines, test_lines = train_test_split(lines, test_size=0.2, random_state=42)
train_lines, val_lines = train_test_split(train_lines, test_size=0.2, random_state=42)

# Print the number of lines in each set
print("Number of lines in training set:", len(train_lines))
print("Number of lines in test set:", len(test_lines))
print("Number of lines in validation set:", len(val_lines))

print('Loading GPT2')
# Define a custom dataset
class TextDataset(Dataset):
    def __init__(self, lines, tokenizer, max_length):
        self.lines = lines
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, idx):
        line = self.lines[idx]['text']
        encoding = self.tokenizer.encode_plus(
            line,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        input_ids = encoding['input_ids'].squeeze()
        attention_mask = encoding['attention_mask'].squeeze()
        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask
        }

# Load the GPT-2 model and tokenizer
model_name = 'gpt2'
print(' - loading gpt 2 head model')
model = GPT2LMHeadModel.from_pretrained(model_name)
print(' - loading gpt 2 tokenizer model')
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
print(' - done loading gpt 2')

# Set the device to GPU if available
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(device)

print('Specifying params')
# Define the hyperparameters
batch_size = 8
max_length = 512
num_epochs = 5
learning_rate = 1e-5

# Create dataloaders for training, validation, and testing
train_dataset = TextDataset(train_lines, tokenizer, max_length)
val_dataset = TextDataset(val_lines, tokenizer, max_length)
test_dataset = TextDataset(test_lines, tokenizer, max_length)

train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_dataloader = DataLoader(val_dataset, batch_size=batch_size)
test_dataloader = DataLoader(test_dataset, batch_size=batch_size)

# Define the optimizer and loss function
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
criterion = torch.nn.CrossEntropyLoss()

# Set the padding token
tokenizer.pad_token = tokenizer.eos_token

print('Training model for ',num_epochs,' epochs, using AdamW')

# Training loop
for epoch in range(num_epochs):
    model.train()
    total_loss = 0

    print('    [at Epoch ',epoch,'/',num_epochs,']')

    for batch in train_dataloader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=input_ids)
        loss = outputs.loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(train_dataloader)
    print(f"Epoch {epoch+1}/{num_epochs} - Average Loss: {avg_loss}")

# Evaluation on validation set
model.eval()
total_loss = 0

with torch.no_grad():
    for batch in val_dataloader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=input_ids)
        loss = outputs.loss

        total_loss += loss.item()

avg_loss = total_loss / len(val_dataloader)
print(f"Validation Loss: {avg_loss}")

# Evaluation on test set
model.eval()
total_loss = 0

with torch.no_grad():
    for batch in test_dataloader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=input_ids)
        loss = outputs.loss

        total_loss += loss.item()

avg_loss = total_loss / len(test_dataloader)
print(f"Test Loss: {avg_loss}")

# Save the trained model
torch.save(model.state_dict(), 'sample.safetensor')