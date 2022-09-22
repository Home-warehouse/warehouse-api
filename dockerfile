### Stage 1: build ui app ###
FROM node:14.16.0-alpine as ui_builder
LABEL maintainer="Daniel Goliszewski taafeenn@gmail.com"
LABEL version="0.3.4"

# Set working directory.
RUN mkdir -p /build_dir/output 
WORKDIR /build_dir 

# Copy app dependencies.
COPY ../home-warehouse-ui/package*.json /build_dir/
# Install app dependencies.
RUN npm install

# Copy app files.
COPY ../home-warehouse-ui /build_dir

RUN printf "export const environment = { production: true, apiIP: 'api/', intergrations: [ { name: 'EVERNOTE', integrated: false } ] };" > src/environments/environment.prod.ts; npm run build -- --output-path=/build_dir/output

### Stage 2: serve ###
FROM python:3.9-alpine3.13
LABEL maintainer="Daniel Goliszewski taafeenn@gmail.com"
LABEL version="0.3.4"

# Set working dir
WORKDIR /usr/src/app/home-warehouse

# Install API deps
COPY ../home-warehouse-api/requirements.txt /usr/src/app/home-warehouse
RUN apk add --update musl-dev gcc libffi-dev git
RUN pip install -r requirements.txt
COPY ../home-warehouse-api /usr/src/app/home-warehouse

# Copy app
COPY --from=ui_builder /build_dir/output /usr/src/app/home-warehouse/home_warehouse_api/app

EXPOSE 8000
CMD ["python", "/usr/src/app/home-warehouse/home_warehouse_api/main.py"]