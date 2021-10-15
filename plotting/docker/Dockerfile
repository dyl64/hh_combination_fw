FROM ubuntu:20.04
LABEL maintainer="Rui Zhang (rui.zhang@cern.ch)"

RUN apt-get update -y && \
    apt-get install -y \
        fontconfig \
        fonts-dejavu \
        fonts-freefont-ttf \
        python3 \
        python3-dev \
        python3-pip \
        python3-venv \
        vim && \
        apt-get -y autoclean && \
        apt-get -y autoremove && \
        rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade --no-cache-dir pip setuptools wheel && \
    python3 -m pip install --no-cache-dir "mplhep~=0.2.9" && \
    python3 -m pip install --no-cache-dir "atlas_mpl_style~=0.20.0" click pandas uproot && \
    python3 -m pip list

RUN alias python='python3'

WORKDIR /workarea
COPY docker/atlas_mpl_style.patch /workarea/
RUN patch /usr/local/lib/python3.8/dist-packages/atlas_mpl_style/plot.py atlas_mpl_style.patch
