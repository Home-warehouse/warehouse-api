FROM python:3.9-alpine3.13
MAINTAINER Daniel Goliszewski "taafeenn@gmail.com"
LABEL version="0.3.0"
WORKDIR /usr/src/app/home-warehouse-api
COPY requirements.txt ./
RUN apk add --update musl-dev gcc libffi-dev git
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "home_warehouse_api/main.py"]