FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PEAK_URL=https://github.com/kryptex-miners-org/kryptex-miners/releases/download/peakminer-2-18-3/peakminer-2.18.3.tar.gz \
    PEAK_FILE=peakminer-2.18.3.tar.gz \
    PEAK_SHA256= \
    PEAK_ARGS=

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        wget \
        ca-certificates \
        tar \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --system --create-home --home-dir /home/miner miner \
    && mkdir -p /opt/peakminer \
    && chown -R miner:miner /opt/peakminer

WORKDIR /opt/peakminer

COPY task.py /opt/peakminer/task.py
RUN chown miner:miner /opt/peakminer/task.py \
    && chmod 755 /opt/peakminer/task.py

USER miner

ENTRYPOINT ["python3", "/opt/peakminer/task.py"]
