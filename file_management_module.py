
# AI-enhanced file operations
from gen_ai_utils import generate_text

def ai_handle_file_operations(operation, details):
    instruction = f"{operation} with these details: {details}"
    return generate_text(instruction)
