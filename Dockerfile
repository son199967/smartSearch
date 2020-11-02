FROM python:3.8-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN apk update \
     &&  apk add --upgrade --no-cache \
	python3 libpq uwsgi-python3 \
	python3-dev py3-pip alpine-sdk postgresql-dev postgresql \
	proj proj-dev \
	proj-util \
        bash openssh curl ca-certificates openssl less htop \
	g++ make wget rsync \
        build-base libpng-dev freetype-dev libexecinfo-dev openblas-dev libgomp lapack-dev \
        libgcc libquadmath musl  \
	libgfortran \
	lapack-dev \
     &&  pip install --no-cache-dir --upgrade pip \
     &&  pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]