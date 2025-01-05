# ai-document-api-python
# Description
This is a Python (Flask) based API for AI document editing, available for free public use.

## IMPORTANT: place your Gemini API into constants.py file ([Google AI Studio](https://aistudio.google.com/app/apikey))
(create an account if needed)
1. Create API Key and place it into constants.py

## Prerequisites
- Python 3.9 or higher ([Download](https://www.python.org/downloads/))
- Virtual Environment ([Documentation](https://docs.python.org/3/library/venv.html))

### Optional Dependencies
Docker ([Install](https://docs.docker.com/engine/install/))

## Local Development Setup
1. Create virtusl environment
> python3 -m venv .venv

2. Install packages
> pip install -r requirements.txt

3. Run server:
> python server.py

## Docker Setup
1. Install - Docker ([Installation Guide](https://docs.docker.com/engine/install/))

2. Build docker image using bash script
> ./run_docker.sh

3. Stop docker container and remove image using bash script
> ./remove_docker_container.sh

## For contributors:
1. Create a new branch
2. Validate your change with Pylint
>> pylint --rcfile=pyproject.toml .
3. Commit and push your changes for review

Thank you!