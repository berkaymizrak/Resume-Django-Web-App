###########
# BUILDER #
###########

# pull official base image
FROM python:3.9.1-slim as builder

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
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade virtualenv && python -m virtualenv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ADD $REPO_PATH/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /tmp/wheels -r /tmp/requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.9.1-slim

# create the app user
RUN addgroup app && useradd app -g app

RUN apt-get update
# install dependencies
RUN apt-get install libpq-dev python3-dev -y
RUN apt-get install build-essential -y
# Install Postgres alive checker (pg_isready)
RUN apt install -y postgresql-client

COPY --from=builder /tmp/wheels /wheels
COPY --from=builder /tmp/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy entrypoint.prod.sh
COPY entrypoint.prod.sh /srv/entrypoint.prod.sh
RUN sed -i 's/\r$//g' /srv/entrypoint.prod.sh
RUN chmod +x /srv/entrypoint.prod.sh

COPY $REPO_PATH /srv/app_resume
# set work directory
WORKDIR /srv/app_resume

# chown all the files to the app user
RUN chown -R app:app /srv/app_resume

# change to the app user
USER app

ENTRYPOINT ["/srv/entrypoint.prod.sh"]
