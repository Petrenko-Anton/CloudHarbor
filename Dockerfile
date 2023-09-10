FROM python:3.11

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY poetry.lock $APP_HOME/poetry.lock
COPY pyproject.toml $APP_HOME/pyproject.toml

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --only main

COPY . .
EXPOSE 8000

CMD ["python","WebAppTeam4/manage.py","runserver","0.0.0.0:8000"]
