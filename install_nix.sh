HW_PATH=$1
HW_VERSION=$2
API_HOST=$3
API_PORT=$4
APP_PORT=$5

if [${#HW_VERSION_UI} -eq 0 ]
then
    HW_VERSION_UI = $HW_VERSION
fi

git clone https://github.com/Home-warehouse/warehouse-api.git --depth 1 --branch $HW_VERSION home-warehouse-api
git clone https://github.com/Home-warehouse/warehouse-ui.git --depth 1 --branch $HW_VERSION_UI home-warehouse-ui

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