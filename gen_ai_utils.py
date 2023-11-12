
# gen_ai_utils.py
import google.generativeai as palm
import os

def configure_ai():
    api_key = os.getenv('PALM_API_KEY')
    if not api_key:
        raise EnvironmentError("The PALM_API_KEY environment variable is not set.")
    palm.configure(api_key=api_key)

def generate_text(prompt):
    response = palm.generate_text(prompt=prompt)
    return response.result
