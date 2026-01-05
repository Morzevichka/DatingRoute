FROM python:3.13-alpine AS builder
WORKDIR /install
RUN apk add --no-cache build-base
COPY requirements.txt .
RUN pip install --upgrade pip \
	&& pip wheel \
		--no-cache-dir \
		--wheel-dir /wheels \
		-r requirements.txt

FROM python:3.13-alpine
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

ARG APPLICATION_USER=appuser
RUN adduser --no-create-home -u 1000 -D $APPLICATION_USER
RUN mkdir /app

COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install \
		--no-cache-dir \ 
		--no-index \
		--find-links=/wheels \
		-r requirements.txt \
	&& rm -rf /wheels /root/.cache/pip

COPY . /app

RUN chown -R $APPLICATION_USER /app \
	&& chmod 755 -R /app

WORKDIR /app

USER 1000

EXPOSE 8082

ENTRYPOINT [ "python", "-m", "uvicorn", "ai:app" ]
