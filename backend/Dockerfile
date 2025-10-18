FROM python:3.11-slim


COPY ../pyproject.toml ../poetry.lock* ./

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --only=main --no-root

COPY . .
WORKDIR /backend
EXPOSE ${PORT:-8000}

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
