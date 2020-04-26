FROM python:3.8.2-slim-buster

RUN apt-get update && apt-get install -y \
  binutils \
  gdal-bin \
  libgdal-dev \
  python3-gdal \
  binutils \
  libproj-dev \
  wget

RUN apt-get install bash
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# download the cloudsql proxy
RUN wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 --output-document /usr/src/app/cloud_sql_proxy
# make cloudsql proxy executable
RUN chmod +x /usr/src/app/cloud_sql_proxy

RUN ln -sf /dev/stdout /var/log/access.log && \
    ln -sf /dev/stderr /var/log/error.log

ADD . /usr/src/app
WORKDIR /usr/src/app
# RUN dir
ENTRYPOINT ["bash", "run.sh"]