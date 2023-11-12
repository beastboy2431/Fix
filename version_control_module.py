
# AI-enhanced version control operations
from gen_ai_utils import generate_text

def ai_generate_commit_message(changes_description):
    commit_message = generate_text(f"Generate a commit message for these changes: {changes_description}")
    return commit_message
