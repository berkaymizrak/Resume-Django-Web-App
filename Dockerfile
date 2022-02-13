FROM python:3.9.1-slim
ARG REPO_PATH
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/opt/venv

RUN apt-get update
# Install Postgres
RUN #apt-get install libpq-dev -y
# Update pip
RUN pip install --upgrade pip
# Create venv
RUN pip install virtualenv && python -m virtualenv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ADD $REPO_PATH/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY entrypoint.sh /srv/entrypoint.sh

COPY $REPO_PATH /srv/app_resume
WORKDIR /srv/app_resume

ENTRYPOINT ["/srv/entrypoint.sh"]
