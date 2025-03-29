# Define the virtual environment directory
PROJECT=aklab
VENV_DIR=~/08-STSFE/venv/$(PROJECT)

# Define the commands
UNAME_S := $(shell uname -s)

# The Ubuntu installation uses the Lambda stack
ifeq ($(UNAME_S),Linux)
    PYTHON_VENV_CMD=python -m venv --system-site-packages $(VENV_DIR)
endif

ifeq ($(UNAME_S),Darwin)
    PYTHON_VENV_CMD=/usr/local/bin/python3.10 -m venv $(VENV_DIR)
endif

# Check the shell and define the activation command accordingly
SHELL:=/bin/bash  # Avoid using system shell, which is dash on Ubuntu
ACTIVATE_CMD=source $(VENV_DIR)/bin/activate
UPGRADE_PIP_CMD=pip install --upgrade pip 
INSTALL_PYTEST=pip install -U pytest pytest-cov
INSTALL_CONTEXERE=cd ../contexere;pip install -e .;cd ../$(PROJECT)
INSTALL_DEV=pip install -e .
INSTALL_KERNEL=ipython kernel install --user --name $(PROJECT)

# Default target
all: venv

# Create virtual environment
venv:
	$(PYTHON_VENV_CMD)
	$(ACTIVATE_CMD) && $(UPGRADE_PIP_CMD)
	$(ACTIVATE_CMD) && $(INSTALL_PYTEST)
	$(ACTIVATE_CMD) && $(INSTALL_CONTEXERE)
	$(ACTIVATE_CMD) && $(INSTALL_DEV)
	$(ACTIVATE_CMD) && $(INSTALL_KERNEL)

activate:
	@echo "#!/bin/sh" > activate_venv.sh
	@echo "$(ACTIVATE_CMD)" >> activate_venv.sh
	@chmod +x activate_venv.sh
	@echo "Run 'source activate_venv.sh' to activate the virtual environment."

# Clean target to remove the virtual environment
clean:
	rm -rf $(VENV_DIR)
