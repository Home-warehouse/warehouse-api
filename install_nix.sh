git clone https://github.com/Home-warehouse/warehouse-api.git home-warehouse-api
git clone https://github.com/Home-warehouse/warehouse-ui.git home-warehouse-ui

HW_PATH=$1
API_HOST=$2
API_PORT=$3
APP_PORT=$4

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
API_HOST=0.0.0.0
API_PORT=$API_PORT
API_ORIGINS=['*']
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
  apiIP: 'http://$API_HOST:$API_PORT/',
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