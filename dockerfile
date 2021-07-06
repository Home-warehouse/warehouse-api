FROM python:3.9-alpine3.13
MAINTAINER Daniel Goliszewski "taafeenn@gmail.com"
WORKDIR /usr/src/app/home-warehouse-api
COPY requirements.txt ./
RUN pip install requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "home_warehouse_api/main.py"]