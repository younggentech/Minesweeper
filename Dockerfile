FROM python:3.11-slim-bookworm
COPY req.txt .
COPY secrets ./secrets
COPY __init__.py .
COPY games.pickle .
COPY main.py .
COPY users.pickle .
COPY bot/game ./bot/game
COPY bot/__init__.py ./bot
COPY bot/additional_classes.py ./bot
COPY bot/button_texts.py ./bot
COPY bot/handlers.py ./bot
COPY bot/keyboard_generator.py ./bot
COPY bot/messages.py ./bot
RUN pip install -r req.txt
CMD ["python3", "main.py"]
