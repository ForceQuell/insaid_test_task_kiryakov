FROM python:3.10-slim-buster

WORKDIR /app
 
COPY ./ /app
RUN rm Pipfile.lock && rm .env

RUN pip3 install pipenv
RUN pipenv install
RUN chmod +x start.sh

ENV PYTHONPATH="/app/src"

EXPOSE 80

CMD cd src && pipenv run alembic upgrade head && cd ../ && pipenv run uvicorn main:app --host 0.0.0.0 --port 80
