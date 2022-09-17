FROM python:3.9-alpine3.13
LABEL maintainer="Daniel Goliszewski taafeenn@gmail.com"
LABEL version="0.3.4"
WORKDIR /usr/src/app/home-warehouse-api
COPY requirements.txt ./
RUN apk add --update musl-dev gcc libffi-dev git
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "home_warehouse_api/main.py"]