FROM debian:bookworm-slim

ENV PEAK_URL="https://github.com/kryptex-miners-org/kryptex-miners/releases/download/peakminer-2-18-3/peakminer-2.18.3.tar.gz"
ENV PEAK_FILE="peakminer-2.18.3.tar.gz"
ENV PEAK_DIR="/opt/peakminer"

# default wallet/coin/pool (bisa override via -e ...)
ENV WALLET="prl1pjp3jd7ue653f6zyrn9ewwu7lalw538kn5w2l4lekv0g3nxqlj23qnwg6g0"
ENV COIN="pearl"
ENV POOL="stratum+tcp://prl.kryptex.network:7048"

RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 wget tar ca-certificates \
 && rm -rf /var/lib/apt/lists/*

COPY task.py /task.py
RUN chmod +x /task.py

ENTRYPOINT ["python3", "/task.py"]
