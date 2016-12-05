FROM python:2.7

ENV UWSGI_PROCESSES 8
ENV UWSGI_THREADS 10

WORKDIR /opt/zvooq

COPY src/requirements.txt requirements.txt

# first time (ususally cached by Docker)
RUN pip install --upgrade --requirement requirements.txt

COPY src .

# second time (upgrade all requirements)
RUN pip install --upgrade --requirement requirements.txt

COPY etc/uwsgi/uwsgi.ini /etc/zvooq/uwsgi.ini

EXPOSE 8000

CMD ["uwsgi", "--ini", "/etc/zvooq/uwsgi.ini"]
