FROM python:3.9

ENV POETRY_VERSION=1.2.1

#System dependencies
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app/

COPY web/pyproject.toml /app/
COPY web/poetry.lock /app/

RUN poetry env use 3.9
RUN poetry install

COPY source /app/source/

RUN mkdir -p /app/config/

CMD ["poetry", "run", "python", "-m", "source.web.main"]
