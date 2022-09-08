# ## Install Python Dependencies
update-environment:
	pip3 install -r requirements.txt

#activate new env
SHELL := /bin/bash
activate-env :
	. .venv/bin/activate && exec $$SHELL

#set path
path:
	export PYTHONPATH="./app:./tests"

## Run unit tests
test:
	pytest --asyncio-mode=auto --cov-report html --cov=FASTApi/app ./tests

## Sort requirements files
sort-deps:
	@printf "Sorting requirements file\n"
	@cat requirements.txt | grep "\S" | sed -E 's/^[[:blank:]]*//' | sort --ignore-case -o requirements.txt

## Run vulture to find dead code
run-vulture:
	@printf ">>> Running Vulture to search for dead code\n"
	# To ignore errors in a command line,
	# write a '-' at the beginning of the line's text (after the initial tab).
	# The '-' is discarded before the command is passed to the shell for execution.
	# This will allow the build continue even if vulture finds problems in the code.
	# This will also add the code that is reported as unused to whitelist.py
	# Remember vulture is used here a warning tool, to show what code could be removed.
	-vulture similarity  --make-whitelist > whitelist.py
	@printf ">>> Vulture finished\n"

## Format my code via pre-commit hooks
format:
	@echo "Running code formatting via pre-commit hooks"
	pre-commit run --files ./* ./app/* ./tests/*

## Removed the build, dist directories, pycache, pyo or pyc and swap files
clean:
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type f -name '*.py[co]' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -type f -name '.DS_Store' -delete
	@echo ">>> Removed pycache, .pyc, .pyo, .DS_Store files and files with ~"
help:
	@echo "Help: list of available commands:"
	@grep -o '^[a-z-][^:]*' Makefile



#########################################################
###################### FASTApi ###########################
#########################################################
dev: update-environment
	uvicorn app.main:app --reload --log-config=../log_config_local.yaml

start:
	uvicorn app.main:app --log-config=../log_config.yaml

#########################################################
###################### Docker ###########################
#########################################################
build:
	@echo "Building a test image for the FASTApi service..."
	@docker build . --build-arg SERVICE=FASTApi  -f ../services/Dockerfile -t bla:yep1

push:
	@echo "Pushing test image to Azure Registry..."
	@az acr login --name dgscudscr01
	@docker push bla:yep1

checkrun:
	@echo "Checking if the build can run..."
	@docker run --env-file app/dev.env -t bla:yep1

#########################################################
################### Kubernetes ##########################
#########################################################

deploy:
	@echo "Deploy similarity skills to Kubernetes Environment..."
	@kubectl apply -f deployment.yaml


