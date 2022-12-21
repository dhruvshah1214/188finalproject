FROM python:3.9

ENV POETRY_VERSION=1.2.1

#System dependencies
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app/

COPY cron/pyproject.toml /app/
COPY cron/poetry.lock /app/

RUN poetry env use 3.9
RUN poetry install

COPY source /app/source/

RUN mkdir -p /app/config/
RUN mkdir -p /app/storage/

CMD ["poetry", "run", "python", "-m", "source.cron.main"]
