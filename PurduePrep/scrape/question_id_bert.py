# Ideas for training better models
    # Get rid of punctuation

# %%
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from transformers import BertTokenizer, BertModel, AdamW, get_linear_schedule_with_warmup
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import pickle
from tqdm import tqdm
import time
import numpy as np

# %% [markdown]
# Load training data

# %%
def get_text_two_dfs(fraction):
    with open(f'question_data.pkl', 'rb') as f:
        df = pickle.load(f)
    questions = df[df['labels'] == 1].sample(frac=fraction).reset_index(drop=True)
    questions = questions['text'].values

    with open(f'plaintext.pkl', 'rb') as f:
        df = pickle.load(f)
    sentences = df[df['labels'] == 0].sample(frac=fraction).reset_index(drop=True)
    sentences = sentences['text'].values
    texts = np.append(sentences, questions)
    labels = [0] * len(sentences) + [1] * len(questions)
    return texts, labels

def get_text(fraction):
    with open(f'question_data.pkl', 'rb') as f:
        df = pickle.load(f)

    sentences = df[df['labels'] == 0]['text'].values
    questions = df[df['labels'] == 1]['text'].values
    sentences = sentences[0: int(fraction * len(sentences))]
    questions = questions[0: int(fraction * len(questions))]
    texts = np.append(sentences, questions)
    labels = [0] * len(sentences) + [1] * len(questions)
    return texts, labels
            
texts, labels = get_text_two_dfs(0.01)
print(texts)
print(labels)
print(len(texts), len(labels))

# %% [markdown]
# Transfer learning with BERT from https://medium.com/@khang.pham.exxact/text-classification-with-bert-7afaacc5e49b

# %%
class TextClassificationDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    def __len__(self):
        return len(self.texts)
    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        encoding = self.tokenizer(text, return_tensors='pt', max_length=self.max_length, padding='max_length', truncation=True)
        return {'input_ids': encoding['input_ids'].flatten(), 'attention_mask': encoding['attention_mask'].flatten(), 'label': torch.tensor(label)}

# %%
class BERTClassifier(nn.Module):
    def __init__(self, bert_model_name, num_classes):
        super(BERTClassifier, self).__init__()
        self.bert = BertModel.from_pretrained(bert_model_name)
        self.dropout = nn.Dropout(0.1)
        self.fc = nn.Linear(self.bert.config.hidden_size, num_classes)

    def forward(self, input_ids, attention_mask):
            outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
            pooled_output = outputs.pooler_output
            x = self.dropout(pooled_output)
            logits = self.fc(x)
            return logits

# %%
def train(model, data_loader, optimizer, scheduler, device):
    model.train()

    total_batches = len(data_loader)
    start_time = time.time()

    for batch_idx, batch in enumerate(data_loader):
        optimizer.zero_grad()
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['label'].to(device)
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        loss = nn.CrossEntropyLoss()(outputs, labels)

        # try with/without
        optimizer.zero_grad()
        
        loss.backward()
        optimizer.step()
        scheduler.step()

        elapsed_time = time.time() - start_time
        avg_time_per_batch = elapsed_time / (batch_idx + 1)
        remaining_batches = total_batches - (batch_idx + 1)
        eta = avg_time_per_batch * remaining_batches
        
        # Update tqdm progress bar with ETA
        epoch_progress.set_postfix(loss=loss.item(), eta=f"{eta:.2f}s")
        epoch_progress.update(1)

def evaluate(model, data_loader, device):
    model.eval()
    predictions = []
    actual_labels = []
    with torch.no_grad():
        for batch in data_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['label'].to(device)
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            _, preds = torch.max(outputs, dim=1)
            predictions.extend(preds.cpu().tolist())
            actual_labels.extend(labels.cpu().tolist())
    return accuracy_score(actual_labels, predictions), classification_report(actual_labels, predictions)

def predict_question(text, model, tokenizer, device, max_length=128):
    model.eval()
    encoding = tokenizer(text, return_tensors='pt', max_length=max_length, padding='max_length', truncation=True)
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)

    with torch.no_grad():
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            _, preds = torch.max(outputs, dim=1)
    return "question" if preds.item() == 1 else "plaintext"

# %% [markdown]
# Training

# %%
print(torch.cuda.is_available())
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
rand_tensor = torch.rand(5,2)
print(f'input is on {rand_tensor.device}')
rand_tensor = rand_tensor.to(device)
print(f'input is on {rand_tensor.device}')


# %%
# Set up parameters
bert_model_name = 'bert-base-uncased'
num_classes = 2
max_length = 128
batch_size = 16
num_epochs = 1
learning_rate = 2e-5

# Retrieve and tokenize data
train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size=0.2, random_state=42)
tokenizer = BertTokenizer.from_pretrained(bert_model_name)
train_dataset = TextClassificationDataset(train_texts, train_labels, tokenizer, max_length)
val_dataset = TextClassificationDataset(val_texts, val_labels, tokenizer, max_length)
train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_dataloader = DataLoader(val_dataset, batch_size=batch_size)

# Define model
model = BERTClassifier(bert_model_name, num_classes).to(device)

# Set parameters
optimizer = AdamW(model.parameters(), lr=learning_rate)
total_steps = len(train_dataloader) * num_epochs
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)

# Train
for epoch in range(num_epochs):
        print(f"Epoch {epoch + 1}/{num_epochs}")
        epoch_progress = tqdm(train_dataloader, desc="Training", total=len(train_dataloader), dynamic_ncols=True, leave=True)
        train(model, epoch_progress, optimizer, scheduler, device)
        accuracy, report = evaluate(model, val_dataloader, device)
        print(f"Validation Accuracy: {accuracy:.4f}")
        print(report)

# %% [markdown]
# Save model

# %%
torch.save(model.state_dict(), "bert_classifier.pth")

# %%
test_text = "this is a set of plaintext found on a website. it is two sentences."
isQ = predict_question(test_text, model, tokenizer, device)
print(f"Prediction: {isQ}")

# %%
