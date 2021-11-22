FROM ubuntu
#WORKDIR .
# install psql
RUN apt-get update
RUN apt-get -y install postgresql-client

RUN echo 'hi !!!!!!!!!'
RUN pwd
ADD ./.initdb/init.sql /docker-entrypoint-initdb.d/
ADD ./.initdb/make_echo.sh /docker-entrypoint-initdb.d/
