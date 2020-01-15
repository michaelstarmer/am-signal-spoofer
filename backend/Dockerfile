FROM node:10
LABEL maintainer=michael@ways.no
RUN apt-get update && apt-get install -y locales tzdata
RUN sed -i -e 's/# nb_NO.UTF-8 UTF-8/nb_NO.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=nb_NO.UTF-8
ENV LANG='nb_NO.UTF-8' LANGUAGE='nb_NO:no' LC_ALL='nb_NO.UTF-8'
RUN cp /usr/share/zoneinfo/Europe/Oslo /etc/localtime
RUN locale -a

RUN npm i -g @adonisjs/cli

COPY ./src /src

WORKDIR /src
RUN ls -la /src
RUN npm i

CMD ["nodejs", "server.js"]
