FROM ubuntu:oracular

ADD ./placards /app/placards
ADD ./setup.py /app/
ADD ./install.sh /app/
ADD ./docker/entrypoint.sh /entrypoint.sh
ADD ./placards.ini /etc/pacards/config.ini
RUN chmod +x /entrypoint.sh

RUN apt-get update && apt-get install curl gnupg python3-pip python3-setuptools sudo xauth -y \
  && pip install --upgrade --break-system-packages setuptools \
  && curl --location --silent https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
  && apt-get update \
  && apt-get install google-chrome-stable -y --no-install-recommends \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -d /home/placards placards && \
    mkdir -p /home/placards && \
    chown placards:placards /home/placards

WORKDIR /app

RUN CHROME_USER=placards ./install.sh

ENTRYPOINT [ "/entrypoint.sh" ]
