# pull official base image
FROM python:3.9.1-slim

# set environment variables
ARG REPO_PATH
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/opt/venv

RUN apt-get update
# Install Postgres requirements
RUN apt-get install libpq-dev python3-dev -y
RUN apt-get install build-essential -y
# Install Postgres alive checker (pg_isready)
RUN apt install -y postgresql-client

# pip requirements
RUN pip install --upgrade pip
RUN pip install virtualenv && python -m virtualenv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ADD $REPO_PATH/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY entrypoint.dev.sh /srv/entrypoint.dev.sh
RUN sed -i 's/\r$//g' /srv/entrypoint.dev.sh
RUN chmod +x /srv/entrypoint.dev.sh

COPY $REPO_PATH /srv/app_resume
# set work directory
WORKDIR /srv/app_resume

ENTRYPOINT ["/srv/entrypoint.dev.sh"]
