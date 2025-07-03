FROM python:3.13-alpine

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    libpq \
    build-base

ARG UID=1000
ARG GID=1000

RUN addgroup -g ${GID} appgroup && \
    adduser -D -u ${UID} -G appgroup -h /home/appuser appuser

WORKDIR /home/appuser/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appgroup /home/appuser

USER appuser

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
