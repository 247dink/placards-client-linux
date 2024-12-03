FROM ubuntu:oracular

ENV PIP_BREAK_SYSTEM_PACKAGES=1

ADD placard /app/placard
ADD Pipfile Pipfile.lock /app/
ADD docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN apt-get update && apt-get install curl gnupg python3-pip sudo xauth -y \
  && curl --location --silent https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
  && apt-get update \
  && apt-get install google-chrome-stable -y --no-install-recommends \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -d /home/dsign dsign && \
    mkdir -p /home/dsign && \
    chown dsign:dsign /home/dsign

WORKDIR /app

RUN pip install pipenv && \
    pipenv install --system

ENTRYPOINT [ "/entrypoint.sh" ]
