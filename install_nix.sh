
git clone https://github.com/Home-warehouse/warehouse-api.git home-warehouse-api
git clone https://github.com/Home-warehouse/warehouse-ui.git home-warehouse-ui

HW_PATH=$1
API_PORT=$2
APP_PORT=$3

# Variables
JWT_SECRET=$RANDOM
EVERNOTE_INTEGRATED=true

# Updated docker .env
printf "API_DIR=$HW_PATH/api
DB_DIR=$HW_PATH/db
API_PORT=$API_PORT
APP_PORT=$APP_PORT" > home-warehouse-api/docker/.env


# Update API .env
printf "DEBUG=False
DB_URL=mongodb://mongo:27017/home-warehouse
API_HOST=127.0.0.1
API_PORT=$API_PORT
API_ORIGINS=['http://localhost:4200', 'http://localhost:8000']
API_JWT_SECRET=$JWT_SECRET" > home-warehouse-api/.env

if [ ${#EVERNOTE_TOKEN} -gt 0 ]
then
    printf "INTEGRATION_EVERNOTE_TOKEN='$EVERNOTE_TOKEN'" >> home-warehouse-api/.env
else
    EVERNOTE_INTEGRATED=false
fi


# Update UI .env
printf "export const environment = {
  production: true,
  apiIP: '',
  intergrations: [
        {
            name: 'EVERNOTE',
            integrated: $EVERNOTE_INTEGRATED
        }
    ]
};" > home-warehouse-ui/src/environments/environment.prod.ts


cd home-warehouse-api/docker
docker-compose build
docker-compose up -d