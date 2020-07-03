FROM python:3.6-buster
ADD requirements.txt /root/requirements.txt
RUN apt-get update -q \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    openmpi-bin \
    libgirepository1.0-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN cat /root/requirements.txt | xargs -n 1 -L 1 pip install
ADD . /root/
USER sme
CMD sh /root/run_policy_based_ge_montezuma.sh
