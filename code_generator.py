
import os
from transformers import pipeline

generator = pipeline('text-generation', model=os.path.join('models', 'CodeLlama-13b-Instruct-hf'))

def generate_code(prompt):
    generated = generator(prompt, max_length=256, num_return_sequences=1)
    return generated[0]['generated_text']
