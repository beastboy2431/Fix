
from gen_ai_utils import generate_text

import spacy

nlp = spacy.load("en_core_web_sm")

def process_input(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

from textblob import TextBlob

def analyze_sentiment(text):
    # Create a TextBlob object
    testimonial = TextBlob(text)
    # This will return a tuple of form (polarity, subjectivity)
    # Polarity is a float within the range [-1.0, 1.0]
    # Subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective
    return testimonial.sentiment

# Example usage
text = "I love this project, it's amazing!"
sentiment = analyze_sentiment(text)
print(f"Sentiment of the text: Polarity - {sentiment.polarity}, Subjectivity - {sentiment.subjectivity}")

def enhanced_entity_recognition(prompt):
    # New functionality using generative AI
    response = generate_text(prompt=f"Identify entities in this text: {prompt}")
    entities = response.result  # Assuming the AI provides a structured response of entities
    return entities

# Enhanced entity recognition function using generative AI
from gen_ai_utils import generate_text

def enhanced_entity_recognition(prompt):
    return generate_text(f"Identify entities in this text: {prompt}")
