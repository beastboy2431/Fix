
# AI-enhanced user interaction
from gen_ai_utils import generate_text

def ai_interact_with_user(user_query):
    response = generate_text(f"Interact with the user query: {user_query}")
    return response
