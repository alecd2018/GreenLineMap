FROM ubuntu:18.04

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

RUN apt-get update

RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 

RUN conda create -n mbta python=3.7

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "mbta", "/bin/bash", "-c"]

# install Flask via conda
RUN conda install flask

# install requests via pip
RUN pip install requests

# install ws281x library
RUN pip install rpi_ws281x

# The code to run when container is started:
COPY main.py .
ENTRYPOINT ["conda", "run", "-n", "mbta", "python", "main.py"]