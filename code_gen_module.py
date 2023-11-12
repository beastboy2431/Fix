
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class CodeGenerationModule:
    def __init__(self):
        # Load the tokenizer and model from Hugging Face Model Hub
        self.dolphin_tokenizer = AutoTokenizer.from_pretrained("ehartford/dolphin-2.2.1-mistral-7b")
        self.dolphin_model = AutoModelForCausalLM.from_pretrained("ehartford/dolphin-2.2.1-mistral-7b")

        self.codellama_tokenizer = AutoTokenizer.from_pretrained("codellama/CodeLlama-13b-Instruct-hf")
        self.codellama_model = AutoModelForCausalLM.from_pretrained("codellama/CodeLlama-13b-Instruct-hf")

    def generate_code(self, prompt):
        # Encode the prompt text to input ids
        input_ids = self.codellama_tokenizer(prompt, return_tensors="pt").input_ids

        # Generate code using the model
        generated_ids = self.codellama_model.generate(input_ids, max_length=512, temperature=0.7)
        
        # Decode the generated ids to text
        generated_code = self.codellama_tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        return generated_code

    def refine_code(self, prompt):
        # For refinement, we can use the dolphin model, which has been trained for more conversational and empathetic responses
        input_ids = self.dolphin_tokenizer(prompt, return_tensors="pt").input_ids

        # Refine code using the model
        refined_ids = self.dolphin_model.generate(input_ids, max_length=512, temperature=0.7)

        # Decode the refined ids to text
        refined_code = self.dolphin_tokenizer.decode(refined_ids[0], skip_special_tokens=True)
        return refined_code
