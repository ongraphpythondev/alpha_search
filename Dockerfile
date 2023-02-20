# Dockerfile

# pull the official docker image
FROM python:3.8.16

# set work directory
WORKDIR /code

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.text .
RUN pip install -r requirements.text

EXPOSE 8000

# copy project
COPY . /code

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
