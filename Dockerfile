FROM ubuntu:20.04


ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt install -y python3 && \
    apt install -y python3-pip && \
    apt install -y python3-enchant && \
    apt install -y graphviz

COPY requirements.txt /opt/deps/requirements.txt
RUN pip3 install -r /opt/deps/requirements.txt

WORKDIR /opt/shared
ENTRYPOINT ["ablog"]
CMD ["build"]
