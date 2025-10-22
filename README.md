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

Navigate to http://localhost:8002
```

## Backend

```
# Lint

docker exec -it path-of-the-python-backend-1 uv run ruff check .
```

```
# Test

docker exec -e AVOID_OPENAI_CALL=false -it path-of-the-python-backend-1 uv run pytest
```

## Frontend

```
# Lint

docker exec -it path-of-the-python-frontend-1 npm run lint
```

```
# Test

docker exec -it path-of-the-python-frontend-1 npm run test
```
