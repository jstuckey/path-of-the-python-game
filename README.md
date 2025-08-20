# Path of the Python

A text-based adventure game similar to Colossal Cave Adventure, but based on AI.

The goal is to explore the following technologies:

- Python
- FastAPI
- React
- AI integration

## Run locally

```
docker-compose up --build

Navigate to http://localhost:8000
```

## Lint

```
docker exec -it path-of-the-python-web-1 uv run ruff check .
```

## Test

```
docker exec -it path-of-the-python-web-1 uv run pytest
```
