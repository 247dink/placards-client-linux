FROM ubuntu:oracular

ADD ./placards /app/placards
ADD ./bin /app/bin
ADD ./setup.py /app/
ADD ./docker/entrypoint.sh /entrypoint.sh
ADD ./config.ini /home/placards/.placards/config.ini

RUN chmod +x /entrypoint.sh && \
    apt-get update && apt-get install curl gnupg python3-pip python3-setuptools sudo xauth x11vnc -y && \
    pip install --upgrade --break-system-packages setuptools && \
    curl --location --silent https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/* && \
    cd /app && \
    pip install --break-system-packages . && \
    rm -rf /app && \
    useradd -d /home/placards placards && \
    chown -R placards:placards /home/placards

ENTRYPOINT [ "/entrypoint.sh" ]
