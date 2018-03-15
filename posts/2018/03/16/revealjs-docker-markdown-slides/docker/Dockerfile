FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
  git \
  nodejs \
  nodejs-legacy \
  npm \
&& rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/hakimel/reveal.js.git

RUN cd reveal.js/ && npm install

ADD ./index.html /reveal.js/index.html

EXPOSE 8000

ENTRYPOINT ["npm", "start", "--prefix", "/reveal.js/"]
