
# AI-enhanced debugging
from gen_ai_utils import generate_text

def ai_debug_code(code_snippet, error_log):
    debugging_steps = generate_text(f"Debug this code: {code_snippet} with these errors: {error_log}")
    return debugging_steps
