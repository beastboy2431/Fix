import subprocess
import logging
from logging.handlers import RotatingFileHandler
from sympy import sympify, SympifyError
import nltk
from nltk.corpus import stopwords
import requests
from bs4 import BeautifulSoup
import urllib.parse

# Set up advanced logging with rotation
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler = RotatingFileHandler('problem_solver.log', maxBytes=5*1024*1024, backupCount=2)
log_handler.setFormatter(log_formatter)
logger = logging.getLogger('problem_solver_logger')
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

# Download required NLTK resources if not already present
nltk.download('punkt')
nltk.download('stopwords')

class ProblemSolver:
    def __init__(self, google_api_key=None, cse_id=None):
        self.known_issues = {
            "issue1": "solution1",
            "issue2": "solution2",
            # ... Add more known issues and solutions ...
        }
        self.google_api_key = google_api_key
        self.cse_id = cse_id

    def log_error(self, error):
        logger.exception(f"Error: {error}")

    def execute_command(self, command):
        try:
            command_list = command.split() if isinstance(command, str) else command
            result = subprocess.run(command_list, text=True, capture_output=True, check=True)
            return {"success": True, "output": result.stdout}
        except subprocess.CalledProcessError as e:
            self.log_error(f"Command execution failed: {e}")
            return {"success": False, "error": f"Command execution failed with return code {e.returncode}: {e.stderr}"}
        except Exception as e:
            self.log_error(e)
            raise

    def evaluate_math_expression(self, expression):
        try:
            result = sympify(expression)
            return str(result)
        except SympifyError as e:
            self.log_error(f"Math expression error: {e}")
            return "An error occurred while solving the math expression."

    def is_mathematical_expression(self, expression):
        try:
            sympify(expression)
            return True
        except SympifyError:
            return False

    def is_text_question(self, question):
        question_words = set(stopwords.words('english')) & {'who', 'what', 'when', 'where', 'why', 'how'}
        tokens = set(nltk.word_tokenize(question.lower()))
        return bool(tokens & question_words)

    def google_search_query(self, query):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"
        }
        query_encoded = urllib.parse.quote_plus(query)
        google_search_url = f"https://www.google.com/search?q={query_encoded}"

        try:
            response = requests.get(google_search_url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            search_result = soup.find('div', class_='tF2Cxc')  # The class for a result container

            if not search_result:
                return "No search results found."

            # Extract the title and the snippet
            title = search_result.find('h3').get_text()
            snippet = search_result.find('div', class_='IsZvec').get_text()

            return {
                "title": title,
                "snippet": snippet
            }
        except requests.RequestException as e:
            self.log_error(f"Google search query error: {e}")
            return "An error occurred during Google search query."

    def solve_problem(self, problem):
        try:
            if problem in self.known_issues:
                return self.known_issues[problem]

            if self.is_mathematical_expression(problem):
                result = self.evaluate_math_expression(problem)
                return f"Math Solution: {result}"

            if self.is_text_question(problem):
                result = self.google_search_query(problem)
                return f"Search Result: {result}"

            # Add more problem-solving cases as needed
            return "This problem type is not supported yet."
        except Exception as e:
            self.log_error(e)
            raise

# Example usage
solver = ProblemSolver()

# For a math problem
math_result = solver.solve_problem("2 + 2")
print(math_result)  # Should print the evaluated result

# For a general question
general_question_result = solver.solve_problem("What is the capital of France?")
print(general_question_result)  # Should print the answer from the search query
