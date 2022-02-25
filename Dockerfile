FROM ubuntu:20.04
ENV PYTHONBUFFERED=1
RUN apt-get update && apt-get install -y dnsutils && curl https://nim-lang.org/choosenim/init.sh -sSf | sh \
    && apt-get install -y python3 && apt-get install -y python3-pip && python3 -m pip install --upgrade pip

COPY requirements.txt /app/
SHELL ["pip3", "install", "-r", "/app/requirements.txt"]
COPY  console_version.py docker_entrypoint.sh asyncio_test.py /app/
WORKDIR /app
ENTRYPOINT ["sh", "./docker_entrypoint.sh"]