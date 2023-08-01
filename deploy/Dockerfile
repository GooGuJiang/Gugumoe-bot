FROM python:3.11 as base

# Setting up locales
RUN apt-get update && apt-get install -y locales && \
    locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

# Installing poetry
RUN pip install poetry==1.4.2

# Configuring poetry
RUN poetry config virtualenvs.create false

# Installing additional dependencies
RUN apt-get update && apt-get install -y curl libffi-dev libcairo2
RUN bash -c "$(curl -Ls https://raw.githubusercontent.com/sjlleo/nexttrace/main/nt_install.sh)"

# Setting Working directory
WORKDIR /app


# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/

# Copying actual application
COPY . /app/

# Installing requirements
RUN poetry install --no-dev


CMD ["/usr/bin/python3", "-m", "gugumoe_bot"]

FROM base as dev

RUN poetry install
