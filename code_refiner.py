
import os
from transformers import pipeline

refiner = pipeline('text-generation', model=os.path.join('models', 'ehartforddolphin-2.2.1-mistral-7b'))

def refine_code(code):
    refined = refiner(code, max_length=256, num_return_sequences=1)
    return refined[0]['generated_text']
