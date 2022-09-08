# Services ¯\\_(ツ)_/¯ 

- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Commands](#commands)
    - [Run Cmmands](#run-commands)
- [Using External Resources](#using-external-resources-other-apis-dbs-etc)
    - [Usage](#usage)
- [Traces and Logs](#traces-and-logs)
    - [Traces](#traces)
    - [Logs](#logs)
- [Swagger](#swagger)
## FastAPI

Our services are written using FastAPI https://fastapi.tiangolo.com/tutorial/
## Getting Started
- Python 3.9
- Install datascience package requirements
- Minimum requirements for a FastAPI project:
  - ```
    fastapi>=0.70.0,< 0.71.0
    pydantic<2.0.0
    uvicorn>=0.15.0,<0.16.0
    ddtrace>=0.55.0,<0.56.0
    python-json-logger>=2.0.2,<2.1.0
## Project Structure

Each service should follow the structure 

```
services
├── README.md
├── Dockerfile
├── fast-api
│   └── ...
├── example
│   ├── Makefile
│   ├── README.md
│   ├── requirements.txt
│   ├── deployment.yaml # Contains all the necessary K8s resources │   └── app
│       ├── __init__.py
│       ├── main.py     # Fast API server setup/config
│       ├── router.py   # Service endpoint
│       ├── errors.py   # Custom exception handlers
│       ├── tests.py    # Folder if necessary
│       └── ...         # Any other necessary modules/files for business logic etc.
├── log_config_local.yaml   # Human-readable logs
└── log_config.yaml         # JSON formatted for DD integrations
```

## Commands

Each service should have a Makefile with at least the following:

### Run commands

- `make dev` - local development:
    - starts server in reload mode(restarts server on code changes)
    - specifies local log config
    - disables dd-trace to prevent errors
    - sets up whatever port-forwarding (usually to dev) or other additional things are necessary depending on the service
- `make start` - in cluster:
    - starts server in normal mode
    - specifies cluster log config

## Using External Resources (Other APIs, DBs etc.)

We want to be intentional and consistent in how we connect to external resources, so:
- Ensure we're not wasting CPU recreating connections we already have
    - Instantiate connections on startup
    - Connect once and re-use for the lifetime of the pod
- Handle connecting to and injecting all external resources in the same way
    - Connect to resources on startup where possible
    - Use FastAPIs dependancy system to inject the already connected resources into services

### Usage


## Traces and Logs

The following configuration must be set for each service:

```python
# main.py
from fastapi import FastAPI
from ddtrace import patch, config
...

patch(fastapi=True,logging=True)
app = FastAPI()

config.fastapi['service_name'] = 'example-service'
config.fastapi['span_name'] = 'example-service-request'

...
```

### Traces

```python
# something.py
from ddtrace import tracer
from .example_queries import example_query

def get_something(db_client):
    with tracer.trace(
        name="get_something",
        resource="example-database",
        service="example-service",
    ):
        res = db_client.query(example_query)
    
    return res
```

### Logs

```python
# router.py
import logging

@router.get("/example/route")
async def get_example():
    logger = logging.getLogger("app.get_example")
    logger.info("INFO")
    logger.error("ERROR")

    return 'logs logged'
```

or

```python
# router.py
import logging

@app.on_event("startup")
def startup():
    logging.getLogger("app.startup").info('Starting up...')
```

## Swagger

To populate our swaggerhub, we can take the auto-generated swagger that Fast API produces, modify if necessary and use in the hub config.

1. Start the service
2. go to http://localhost:8000/openapi.json
3. convert to yaml
    - If you copy/paste the json into http://editor.swagger.io it will offer to convert it to yaml
4. make changes if necessary
    - things like custom errors / response codes etc. aren't auto documented
    - again http://editor.swagger.io is your friend
5. add yaml to swaggerhub config in `infra/k8s/api/test/apps/docs`