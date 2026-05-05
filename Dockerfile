FROM python:3.10-slim

RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    gcc libffi-dev musl-dev ffmpeg aria2 python3-pip ntpsec-ntpdate \
    && ntpdate pool.ntp.org || true \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

CMD ["python3", "main.py"]
