FROM ubuntu:20.04 as base

# Setting up locales
RUN apt-get update && apt-get install -y locales && \
    locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

# Installing python and pip
RUN apt-get install -y python3.11 python3-pip

# Installing poetry
RUN pip install poetry==1.5.1

# Configuring poetry
RUN poetry config virtualenvs.create false

# Installing additional dependencies
RUN apt-get install -y curl libffi-dev libcairo2 && \
    bash <(curl -Ls https://raw.githubusercontent.com/sjlleo/nexttrace/main/nt_install.sh)

# Setting Working directory
WORKDIR /app

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/

# Installing requirements
RUN poetry install --no-dev

# Copying actual application
COPY . /app/

CMD ["/usr/bin/python3", "-m", "gugumoe_bot"]

FROM base as dev

RUN poetry install
