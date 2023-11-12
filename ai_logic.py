
import subprocess
import venv
import os
import shutil
import sys
import logging

logging.basicConfig(level=logging.INFO, filename='virtual_environment.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to create a virtual environment and install libraries
def create_virtual_environment(venv_dir, libraries):
    try:
        # Create a virtual environment
        subprocess.run([sys.executable, '-m', 'venv', venv_dir], check=True)
        
        # Activate the virtual environment
        activate_script = os.path.join(venv_dir, 'Scripts', 'activate')
        subprocess.run([activate_script], check=True)
        
        # Install libraries in the virtual environment
        subprocess.run([sys.executable, '-m', 'pip', 'install'] + libraries, check=True)
        
        return True
    except Exception as e:
        logging.error(f"Error creating virtual environment: {e}")
        return str(e)

# Function to execute a command in the virtual environment
def execute_command_in_venv(venv_dir, command):
    try:
        # Activate the virtual environment
        activate_script = os.path.join(venv_dir, 'Scripts', 'activate')
        subprocess.run([activate_script], check=True)
        
        # Execute the command in the virtual environment
        subprocess.run(command, shell=True, check=True)
        
        return True
    except Exception as e:
        logging.error(f"Error executing command in virtual environment: {e}")
        return str(e)

# Function to create a virtual environment, install libraries, and execute a command
def create_and_execute_in_venv(venv_dir, libraries, command):
    try:
        create_result = create_virtual_environment(venv_dir, libraries)
        if create_result is True:
            execute_result = execute_command_in_venv(venv_dir, command)
            return execute_result
        else:
            return create_result
    except Exception as e:
        logging.error(f"Error in create and execute in venv: {e}")
        return str(e)

# Example usage
venv_directory = "my_virtual_env"
required_libraries = ["numpy", "pandas"]
command_to_execute = "python my_script.py"

# Create a virtual environment, install libraries, and execute a command
execution_result = create_and_execute_in_venv(venv_directory, required_libraries, command_to_execute)
if execution_result is True:
    print("Command executed successfully in the virtual environment.")
else:
    print("Error:", execution_result)
