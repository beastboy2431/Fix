import subprocess
import venv
import os
import shutil
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, filename='open_interpreter.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def open_interpreter_and_execute_commands(venv_path, libraries, code):
    try:
        # Create a virtual environment
        venv.create(venv_path, with_pip=True)
        
        # Activate the virtual environment
        activate_script = os.path.join(venv_path, "Scripts" if sys.platform == "win32" else "bin", "activate")
        activate_cmd = f"source {activate_script}" if sys.platform != "win32" else activate_script
        subprocess.run(activate_cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Install required libraries
        for lib in libraries:
            result = subprocess.run(f"pip install {lib}", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                raise Exception(f"Error installing {lib}: {result.stderr.decode()}")
        
        # Execute Python code
        result = subprocess.run([sys.executable, "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, text=True)
        
        # Deactivate the virtual environment (not necessary in script execution, only in interactive shells)
        # Clean up the virtual environment
        shutil.rmtree(venv_path, ignore_errors=True)
        
        if result.returncode == 0:
            return {
                "success": True,
                "output": result.stdout
            }
        else:
            raise Exception(f"Code execution error: {result.stderr}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess error: {e}")
        return {
            "success": False,
            "error": f"Subprocess error: {e}"
        }
    except Exception as e:
        logging.error(f"General error: {e}")
        return {
            "success": False,
            "error": f"General error: {str(e)}"
        }

# Example usage
venv_path = "/path/to/venv"
libraries = ["numpy", "pandas"]
code_to_execute = "import numpy as np; print(np.random.rand(5))"
result = open_interpreter_and_execute_commands(venv_path, libraries, code_to_execute)

if result["success"]:
    print("Code executed successfully.")
    print("Output:")
    print(result["output"])
else:
    print("Error executing code:")
    print(result["error"])
