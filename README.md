# Data scraping API (atlys)

## Description
Data scraping API by means of FastAPI.

## Deployment

### Virtual environment
Command to build virtual environment under project root, it helps  isolate the project from 
other developments so there are no dependencies collisions:
```bash
python -m venv venv/
```

Activate virtual environment:
```bash
source venv/bin/activate
```

Command to install all dependencies from created virtual environment:
```bash
pip install -r requirements.txt
```

Command to run service:
```bash
uvicorn app.main:app
```

More details on uvicorn - [read more](https://www.uvicorn.org) 

### Docker
Command to build image (from the project root folder):
```bash
docker build -t atlys .
```
Command to run service and expose 80 port for access via `http://localhost:4001`
```bash
docker run -d --name atlys -p 4001:80 atlys
```

To see all the configurations and options, go to the Docker image page: 
[uvicorn-gunicorn-fastapi-docker](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)