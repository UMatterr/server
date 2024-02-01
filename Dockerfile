# pull official base image
FROM python:3.11.7-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat-traditional

# install dependencies
RUN pip install --upgrade pip
COPY ./config/django/requirements.txt .
RUN pip install -r requirements.txt

# copy initial data for django
RUN mkdir fixtures
COPY ./config/django/*initial_data.json ./fixtures

# copy entrypoint.sh
COPY ./entrypoint.sh ./entrypoint.sh
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY ./umatter .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]