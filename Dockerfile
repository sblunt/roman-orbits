# Thanks BJ Fulton for teaching me to do this. Much of this is copied from a Dockerfile
# he made for the KPF DRP.

FROM python:3.8-slim

ENV ROMAN_ORBITS=/roman_orbits

# turn off built-in Python multithreading
ENV MKL_NUM_THREADS=1
ENV NUMEXPR_NUM_THREADS=1
ENV OMP_NUM_THREADS=1

RUN mkdir /roman_orbits && \
    apt-get --yes update && \
    apt install build-essential -y --no-install-recommends && \
    apt-get install --yes git vim emacs nano parallel pkg-config libhdf5-dev && \
    /usr/local/bin/python -m pip install --upgrade pip && \
    cd /roman_orbits

WORKDIR /roman_orbits
COPY requirements.txt /roman_orbits

RUN pip install -r requirements.txt

# uncomment to include a dev version of radvel into the container (radvel must be in path)
# COPY radvel /roman_orbits

COPY all_fits /roman_orbits
RUN chmod -R 755 /roman_orbits/*