FROM ubuntu:latest as base

# Avoiding user interaction with tzdata
ENV DEBIAN_FRONTEND=noninteractive

# Installing necessary locales and system dependencies
RUN apt-get update && apt-get install -y locales python3 python3-pip curl libffi-dev libcairo2 && \
    locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    GUGUMOE_BOT_TOKEN="" \
    GUGUMOE_BOT_USERNAME="" \
    GUGUMOE_BOT_MONGODB_URL="" \
    GUGUMOE_BOT_PROXY=""



# Setting up timezone
RUN ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

# Installing poetry
RUN pip install poetry==1.4.2

# Configuring poetry
RUN poetry config virtualenvs.create false

# Running the nexttrace installation script
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
