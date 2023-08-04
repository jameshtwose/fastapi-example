# fastapi-example
An example fastapi REST API that is used in a tutorial to show how to run CICD pipelines with tekton and argo cd.

## Running the API (python)
- Install the dependencies
  - `pip install -r requirements.txt`
- Run the API
  - `uvicorn main:app --reload`

## Running the API (docker)
- Build the docker image
  - `docker build -t fastapi-example .`
- Run the docker image
  - `docker run -d -p 8080:8080 fastapi-example`