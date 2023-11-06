FROM python:3.10

WORKDIR /opt/app
COPY reqs.txt reqs.txt
COPY manage.py manage.py
COPY geos_test geos_test
COPY points points
COPY init.sh init.sh
COPY static static

RUN apt update \
    && apt install -y postgresql-common \
    && apt install -y binutils libproj-dev gdal-bin

RUN sh /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh -v $INSTALL="yes" \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r reqs.txt


EXPOSE 8000/tcp

CMD ["bash", "init.sh"]