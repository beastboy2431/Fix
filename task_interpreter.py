
from transformers import BertTokenizer, BertForSequenceClassification
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')

def interpret_task(task_description):
    inputs = tokenizer(task_description, return_tensors='pt', max_length=512, truncation=True)
    outputs = model(**inputs)
    task_type = torch.argmax(outputs.logits).item()
    return task_type
