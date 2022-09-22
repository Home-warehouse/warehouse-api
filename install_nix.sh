HW_VERSION=$1
API_HOST=$2

if ! [ -v "$HW_VERSION_UI" ]
then
    HW_VERSION_UI=$HW_VERSION
fi

git clone https://github.com/Home-warehouse/warehouse-api.git --depth 1 --branch $HW_VERSION home-warehouse-api
git clone https://github.com/Home-warehouse/warehouse-ui.git --depth 1 --branch $HW_VERSION_UI home-warehouse-ui

# Variables
JWT_SECRET=$RANDOM
EVERNOTE_INTEGRATED=true

# Updated docker .env
printf "API_PORT=$API_PORT
APP_PORT=$APP_PORT" > home-warehouse-api/docker/.env


# Update API .env
printf "PYTHONPATH=./home_warehouse_api
DEBUG=False
TEST=False
MOUNT_APP=True
DB_URL=mongodb://mongo-home-warehouse:27017/home-warehouse
API_HOST=0.0.0.0
API_PORT=8000
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
    apiIP: 'api/',
    intergrations: [
        {
            name: 'EVERNOTE',
            integrated: ${EVERNOTE_INTEGRATED}
        }
    ]
 };" > home-warehouse-ui/src/environments/environment.prod.ts


cd home-warehouse-api/docker
docker-compose -f docker-compose.yml up -d --build