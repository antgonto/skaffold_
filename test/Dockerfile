FROM docker.prod.walmart.com/wce/ca-roots:latest as ca-roots-certs

FROM hub.docker.prod.walmart.com/library/python:3.10-slim

# copy the ca certificates into place
COPY --from=ca-roots-certs /usr/local/share/ca-certificates /usr/local/share/ca-certificates
COPY --from=ca-roots-certs /etc/ssl/certs/ca-certificates.crt  /etc/ssl/certs/ca-certificates.crt

# This line would set to trust connections for packages from repository.walmart.com
RUN touch /etc/apt/apt.conf.d/99verify-peer.conf \
  && echo >>/etc/apt/apt.conf.d/99verify-peer.conf 'Acquire::https::repository.cache.walmart.com::Verify-Peer "false";'

ENV PYTHONUNBUFFERED 1

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV APP_HOME=/home/app/code
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt --index-url https://repository.walmart.com/repository/pypi-proxy/simple/

# add app
COPY . .

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

EXPOSE 3246

CMD python echo.py -b 0.0.0.0

