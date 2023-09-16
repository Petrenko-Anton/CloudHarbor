FROM python:3.11-slim-buster


WORKDIR .

COPY . .


RUN pip install -r requirements.txt


EXPOSE 8000

CMD ["python", "WebAppTeam4/manage.py", "runserver", "0.0.0.0:8000"]
