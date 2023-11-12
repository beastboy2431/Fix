
# AI-enhanced search and summary
from gen_ai_utils import generate_text

def ai_search_and_summarize(topic):
    summary = generate_text(f"Search for {topic} and provide a summary.")
    return summary
