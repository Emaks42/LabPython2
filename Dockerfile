FROM python:3.11 AS builder

COPY requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt
RUN pip install nuitka
WORKDIR /app

COPY . /app

RUN python -m nuitka --follow-imports --include-plugin-directory=src src/main.py

#CMD ["./main.bin"]

FROM scratch
COPY --from=builder /app/main.bin /main.bin
COPY --from=builder /bin /bin
CMD ['./main.bin']
