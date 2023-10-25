FROM python:3.11-slim-bookworm
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ARG TOKEN
ENV TOKEN=$TOKEN
WORKDIR /app
RUN pip install "poetry"
COPY poetry.lock .
COPY  pyproject.toml .
RUN poetry install --no-root
COPY bot ./bot
COPY tests ./tests
COPY main.py .
CMD ["python3", "main.py"]
