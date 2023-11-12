
import subprocess
import sys
import os
import logging
import shutil
import venv
import signal
import textwrap
import toml

# Setup enhanced logging
logger = logging.getLogger('VirtualEnvManager')
logger.setLevel(logging.INFO)

# Create file handler which logs even debug messages
fh = logging.FileHandler('virtual_environment_advanced.log')
fh.setLevel(logging.INFO)

# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

class VirtualEnvManager:
    def __init__(self, venv_name, python_version="3.8"):
        self.venv_name = venv_name
        self.python_version = python_version
        self.python_executable = shutil.which(f"python{python_version}")
        self.venv_path = os.path.join(os.getcwd(), self.venv_name)
        self.pip_path = os.path.join(self.venv_path, 'bin', 'pip') if os.name != "nt" else os.path.join(self.venv_path, 'Scripts', 'pip.exe')
        self.python_path = os.path.join(self.venv_path, 'bin', 'python') if os.name != "nt" else os.path.join(self.venv_path, 'Scripts', 'python.exe')

        if not self.python_executable:
            raise RuntimeError(f"Python {python_version} is not installed or not found in PATH.")
        if os.path.exists(self.venv_path):
            raise RuntimeError(f"The directory '{self.venv_path}' already exists. Please choose a different name or delete the existing directory.")

    def create(self, requirements_file=None):
        try:
            venv.create(self.venv_path, with_pip=True, system_site_packages=False, symlinks=True, clear=True)
            logger.info(f"Virtual environment '{self.venv_name}' created successfully.")
            if requirements_file:
                self.install_packages(requirements_file)
        except Exception as e:
            logger.error(f"Error creating virtual environment: {e}")
            self.cleanup()
            raise

    def install_packages(self, requirements_file):
        try:
            subprocess.check_call([self.pip_path, "install", "-r", requirements_file])
            logger.info(f"Packages from '{requirements_file}' installed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error installing packages: {e.output}")
            self.cleanup()
            raise

    def run_script(self, script_path):
        try:
            result = subprocess.run(
                [self.python_path, script_path], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                check=True
            )
            logger.info(f"Script '{script_path}' output:\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running the script '{script_path}' with exit status {e.returncode}: {e.stderr}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

    def cleanup(self):
        try:
            shutil.rmtree(self.venv_path)
            logger.info(f"Cleaned up virtual environment '{self.venv_name}'.")
        except Exception as e:
            logger.error(f"Failed to clean up virtual environment '{self.venv_name}': {e}")

    def activate(self):
        activate_script = 'bin/activate' if os.name != 'nt' else 'Scripts\\activate'
        activate_path = os.path.join(self.venv_path, activate_script)
        logger.info(f"Run 'source {activate_path}' to activate the virtual environment manually in shell.")
        return activate_path

    def generate_dockerfile(self):
        dockerfile_contents = textwrap.dedent(f"""
        FROM python:{self.python_version}-slim

        WORKDIR /app

        COPY . /app

        RUN python -m venv /venv
        RUN /venv/bin/pip install --upgrade pip

        COPY requirements.txt /app/requirements.txt
        RUN /venv/bin/pip install -r requirements.txt

        CMD [ "/venv/bin/python", "your_script.py" ]
        """)
        with open('Dockerfile', 'w') as dockerfile:
            dockerfile.write(dockerfile_contents)
        logger.info("Dockerfile generated successfully.")

    def load_configuration(self, config_path):
        try:
            with open(config_path, 'r') as config_file:
                config = toml.load(config_file)
            python_version = config.get('python_version')
            requirements_file = config.get('requirements_file')
            if python_version:
                self.python_version = python_version
                self.python_executable = shutil.which(f"python{python_version}")
            if requirements_file:
                self.create(requirements_file=requirements_file)
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise

# Signal handler for graceful exit
def signal_handler(sig, frame):
    logger.info('You pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Example usage with Dockerfile generation:
# manager = VirtualEnvManager("my_advanced_virtual_env", python_version="3.8")
# manager.create(requirements_file="requirements.txt")
# manager.generate_dockerfile()
# manager.run_script("generated_code.py")
