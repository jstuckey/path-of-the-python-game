FROM python:3.13-slim-trixie
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock .
RUN uv sync
COPY . .
EXPOSE 8000

ENTRYPOINT ["uv", "run"]
CMD ["fastapi", "dev", "--host", "0.0.0.0", "main.py"]
