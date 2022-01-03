FROM ubuntu:20.04


ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt install -y python3 && \
    apt install -y python3-pip && \
    apt install -y python3-enchant && \
    apt install -y graphviz && \
    apt install -y git

COPY requirements.txt /opt/deps/requirements.txt
RUN pip3 install -r /opt/deps/requirements.txt

# Applying private fix for https://github.com/abakan/ablog/issues/94
COPY patches/tomorrow.diff /tmp/patches/tomorrow.diff
RUN patch --forward --unified --quiet -d /usr/local/lib/python3.8/dist-packages/ablog < /tmp/patches/tomorrow.diff

# The workdir needs to contain the repo content, e.g. by
# binding it from the host with '-v `pwd`:/opt/shared'
WORKDIR /opt/shared

COPY scripts/mgmt /usr/local/bin
