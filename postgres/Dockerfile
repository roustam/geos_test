FROM postgres:15


RUN apt update && apt install -y postgresql-common
RUN apt install -y postgis postgresql-postgis
RUN sh /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh -v $INSTALL="yes"

ENV POSTGRES_USER=django
ENV POSTGRES_PASSWORD=123qwe
ENV POSTGRES_DB=geo_db
ENV POSTGRES_PORT=5432


EXPOSE 5432/tcp

