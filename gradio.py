
import gradio as gr
import torch
from googlesearch import search
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, filename='ai_assistant.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define functions to load Mistral and CodeLlama models with their respective paths
def load_mistral_model(model_path):
    return torch.hub.load('mistral', model_path)

def load_codellama(model_path):
    return torch.hub.load('codellama', model_path)

# Define the paths to Mistral and CodeLlama models
mistral_model_path = "C:\\Users\\beauc\\OneDrive\\Desktop\\AIAssistantDevTeam\\models\\thebloke-codellama-13b-instruct.Q5_K_M"
codellama_path = "C:\\Users\\beauc\\OneDrive\\Desktop\\AIAssistantDevTeam\\models\\ehartford-dolphin-2.2.1-mistral-7b"

# Initialize Mistral and CodeLlama models using the specified paths
mistral_model = load_mistral_model(mistral_model_path)
codellama = load_codellama(codellama_path)

# Function to generate and improve code autonomously
def generate_and_improve_code(prompt, iterations, token_limit, temperature, web_search=True):
    generated_code = prompt
    for _ in range(iterations):
        try:
            # Use Mistral model to generate code
            mistral_output = mistral_model.generate_code(generated_code, token_limit=token_limit, temperature=temperature)
            # Use CodeLlama model to improve the generated code
            codellama_output = codellama.improve_code(mistral_output)
            generated_code = codellama_output

            if web_search:
                # Search the web for code examples related to the prompt
                query = f"Code example for '{generated_code}'"
                code_results = []
                for j in search(query, num=5, stop=5, pause=2):
                    try:
                        response = requests.get(j)
                        if response.status_code == 200:
                            code_from_web = response.text
                            generated_code += f"\n// Code from the web ({i})\n{code_from_web}"
                        else:
                            generated_code += f"\n// Failed to fetch code from the web ({i})\n"
                    except Exception as e:
                        logging.error(f"Web search error: {e}")
                        generated_code += f"\n// Error fetching code from the web ({i}): {str(e)}\n"
        except Exception as e:
            logging.error(f"Code generation error: {e}")
            return f"An error occurred during code generation: {str(e)}"

    return generated_code

# Function to process files
def process_files(files):
    processed_results = []
    for file in files:
        try:
            # Process each uploaded file (replace with your file processing logic)
            processed_results.append(f"Processed file '{file.name}'")
        except Exception as e:
            logging.error(f"File processing error: {e}")
            processed_results.append(f"Error processing file '{file.name}': {str(e)}")
    return processed_results

# Create Gradio interfaces
iface_code_gen = gr.Interface(
    fn=generate_and_improve_code,
    inputs=[
        "text",
        gr.inputs.Checkbox(default=True, label="Search Web for Code"),
        gr.inputs.Number(label="Iterations", default=5, min=1, max=10),
        gr.inputs.Number(label="Token Limit", default=100, min=10, max=1000),
        gr.inputs.Slider(label="Temperature", default=0.7, min=0.1, max=1.0)
    ],
    outputs="text",
    title="Advanced Code Generation",
    description="Enter a code generation prompt and the system will autonomously generate and improve code.",
    theme="huggingface",
    live=True
)

# Create Gradio interface for file processing
iface_file_processing = gr.Interface(
    fn=process_files,
    inputs=gr.inputs.File(type="multiple", label="Upload Files"),
    outputs="text",
    title="File Processing",
    description="Upload files for processing.",
    theme="huggingface",
    live=True
)

# Combine Gradio interfaces into a single interface
combined_iface = gr.Interface(
    [iface_code_gen, iface_file_processing],
    "tabs",
    title="Advanced AI Assistant",
    description="Collaborative AI Assistant with code generation, web code search, file processing, and more.",
    theme="huggingface",
    live=True
)

# Launch the combined Gradio interface
combined_iface.launch()
